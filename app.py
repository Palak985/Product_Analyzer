import os
import re
import json
import base64
import io
import csv
import random
import requests
import numpy as np # Needed for regression
from datetime import datetime
from collections import Counter
from bs4 import BeautifulSoup
import random
import pandas as pd
import nltk
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from wordcloud import WordCloud

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session, Response
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy 
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer 

# -------------------- CONFIGURATION --------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = 'enterprise_grade_secret_2026'
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
vader = SentimentIntensityAnalyzer()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# -------------------- NLTK SETUP --------------------
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
stop_words.update(['product', 'item', 'one', 'it', 'use', 'good', 'bad', 'review', 'buy', 'bought'])

# -------------------- MODELS --------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="Analyst") 

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    source_link = db.Column(db.String(500))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade="all, delete-orphan")
    analysis = db.relationship('AnalysisResult', backref='product', uselist=False, cascade="all, delete-orphan")

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    clean_text = db.Column(db.Text)
    sentiment = db.Column(db.String(20))
    sentiment_score = db.Column(db.Float)
    is_suspicious = db.Column(db.Boolean, default=False)
    review_date = db.Column(db.DateTime, default=datetime.utcnow)

class AnalysisResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    total_reviews = db.Column(db.Integer)
    pos_count = db.Column(db.Integer)
    neg_count = db.Column(db.Integer)
    neu_count = db.Column(db.Integer)
    ai_verdict = db.Column(db.Text)
    trend_data_json = db.Column(db.Text)
    wordcloud_b64 = db.Column(db.Text) 
    top_keywords_json = db.Column(db.Text)
    aspects_json = db.Column(db.Text)
    forecast_json = db.Column(db.Text)
    insights_json = db.Column(db.Text)
    is_shared = db.Column(db.Boolean, default=True, nullable=False)
    shared_at = db.Column(db.DateTime, nullable=True)

class AnalystProfile(db.Model):
    """Stores aggregated stats about each analyst's work"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True)
    specialty = db.Column(db.String(200), default="General Analysis")  # e.g., "Electronics", "Fashion"
    bio = db.Column(db.Text, default="")
    total_analyses = db.Column(db.Integer, default=0)
    avg_sentiment_score = db.Column(db.Float, default=0.0)
    user = db.relationship('User', backref='profile', uselist=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

# -------------------- HELPERS --------------------
def clean_text_pipeline(text):
    if not isinstance(text, str): return ""
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    text = text.lower().strip()
    return text

def check_if_suspicious(text):
    if len(text.split()) < 3: return True
    if len(set(text.split())) < 2: return True 
    return False

def analyze_aspects(reviews):
    aspects = {
        'Quality': ['quality', 'build', 'material', 'strong', 'durable', 'plastic', 'feel'],
        'Price': ['price', 'value', 'money', 'cost', 'expensive', 'cheap', 'worth'],
        'Performance': ['fast', 'slow', 'lag', 'speed', 'battery', 'charge', 'screen', 'display'],
        'Service': ['service', 'support', 'delivery', 'shipping', 'packaging', 'seller']
    }
    scores = {k: {'pos': 0, 'total': 0} for k in aspects}
    for r in reviews:
        txt = r.clean_text.lower()
        label = r.sentiment
        for aspect, keywords in aspects.items():
            if any(k in txt for k in keywords):
                scores[aspect]['total'] += 1
                if label == 'Positive': scores[aspect]['pos'] += 1
    final_aspects = {}
    for k, v in scores.items():
        if v['total'] > 0: final_aspects[k] = round((v['pos'] / v['total']) * 100)
        else: final_aspects[k] = 0
    return json.dumps(final_aspects)

def calculate_forecast(trend_pos):
    # Simple Linear Regression to predict next point
    if len(trend_pos) < 2: return json.dumps({'direction': 'Stable', 'confidence': 0})
    
    x = np.arange(len(trend_pos))
    y = np.array(trend_pos)
    slope, _ = np.polyfit(x, y, 1)
    
    direction = "Stable"
    if slope > 0.5: direction = "Improving 🚀"
    elif slope < -0.5: direction = "Declining 📉"
    
    return json.dumps({'direction': direction, 'slope': round(slope, 2)})

def generate_wordcloud(text_data):
    if not text_data.strip(): return None
    wc = WordCloud(width=800, height=400, background_color='white', colormap='viridis').generate(text_data)
    img = io.BytesIO()
    wc.to_image().save(img, format='PNG')
    return base64.b64encode(img.getvalue()).decode('utf-8')

def extract_top_keywords(text_list):
    all_words = " ".join(text_list).split()
    filtered_words = [w for w in all_words if w not in stop_words and len(w) > 2]
    return Counter(filtered_words).most_common(10)

def scrape_url(url):
    if "demo" in url.lower():
        return "iPhone 15 Pro", [
            "The battery life is amazing, easily lasts two days!",
            "Camera quality is out of this world, low light photos are crisp.",
            "Overheating issues while charging, very disappointed.",
            "The titanium finish feels premium but it scratches easily.",
            "Best phone I've ever owned, totally worth the price.",
            "Screen refresh rate makes everything feel so smooth.",
            "Face ID is faster than ever.",
            "Too expensive for what it offers compared to the previous model.",
            "I love the new action button, very convenient.",
            "Customer service was unhelpful when I had display issues."
        ]
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.title.string if soup.title else "Scraped Product"
        reviews = [p.get_text() for p in soup.find_all('p') if len(p.get_text()) > 20]
        return title.strip(), reviews[:50]
    except Exception as e:
        return None, str(e)
def generate_verdict(name, total, pos, neg, neu, forecast_direction="Stable"):
    # Calculate percentages
    pos_pct = (pos/total)*100 if total > 0 else 0
    neg_pct = (neg/total)*100 if total > 0 else 0
    
    # Internal Strategy Logic
    def get_strategy(p_pct, f_dir):
        if p_pct > 75 and "Improving" in f_dir:
            return "🚀 STRATEGY: Scale Marketing. Product is in 'Hyper-Growth' phase."
        elif p_pct < 40 or "Declining" in f_dir:
            return "🛠️ STRATEGY: Engineering Review. High churn risk detected; investigate quality."
        else:
            return "🔍 STRATEGY: Periodic Monitoring. Maintain current service levels."

    strategy_text = get_strategy(pos_pct, forecast_direction)

    # Building the HTML Verdict
    verdict = f"<p>After analyzing <strong>{total:,}</strong> reviews for <em>{name}</em>, our AI algorithms indicate:</p>"
    
    if pos_pct > 75: 
        verdict += f"<div style='color:#00b894; font-weight:bold; font-size:1.1rem;'>🏆 Market Leader Performance</div>"
    elif pos_pct > 50: 
        verdict += f"<div style='color:#0984e3; font-weight:bold; font-size:1.1rem;'>📈 Good with Room for Growth</div>"
    elif neg_pct > 40: 
        verdict += f"<div style='color:#d63031; font-weight:bold; font-size:1.1rem;'>⚠️ Critical Attention Needed</div>"
    else: 
        verdict += f"<div style='color:#fdcb6e; font-weight:bold; font-size:1.1rem;'>⚖️ Polarizing Product</div>"

    # Add the automated recommendation box
    verdict += f"""
    <div style="margin-top:15px; padding:12px; background:#f8f9fa; border-radius:8px; border-left:4px solid #6c5ce7;">
        <small style="text-transform:uppercase; color:#6c5ce7; font-weight:800; display:block; margin-bottom:4px;">AI Strategic Advice</small>
        <span style="color:#2d3436; font-weight:600;">{strategy_text}</span>
    </div>
    """
    
    return verdict

# -------------------- ROUTES --------------------

@app.route('/')
def index(): return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            if user.role == 'Admin': return redirect(url_for('admin_panel'))
            return redirect(url_for('dashboard'))
        flash("Invalid credentials", "error")
    return render_template('login.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'Analyst')
        if User.query.filter_by(username=username).first():
            flash("User exists", "error"); return redirect(url_for('register'))
        user = User(username=username, password=generate_password_hash(password), role=role)
        db.session.add(user); db.session.commit()
        flash("Account created! Please login.", "success"); return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user(); return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.role == 'Admin': 
        return redirect(url_for('admin_panel'))
    
    # NEW LOGIC: If Viewer, show all products. If Analyst, show only their own.
    if current_user.role == 'Viewer':
        products = Product.query.order_by(Product.created_at.desc()).all()
    else:
        products = Product.query.filter_by(uploaded_by=current_user.id).order_by(Product.created_at.desc()).all()
    
    # Global Stats for Command Center
    all_data = Product.query.all()
    total_rev = sum(p.analysis.total_reviews for p in all_data if p.analysis and p.analysis.total_reviews)
    
    highest = max((p for p in all_data if p.analysis and p.analysis.total_reviews > 0), 
                  key=lambda x: (x.analysis.pos_count/x.analysis.total_reviews) if x.analysis else 0, default=None)
    
    top_prod = (highest.name, (highest.analysis.pos_count/highest.analysis.total_reviews)*100) if highest and highest.analysis else ("None", 0)

    return render_template('dashboard.html', 
                         products=products, 
                         total_rev=total_rev, 
                         top_prod=top_prod)
@app.route('/public_market')
@login_required
def public_market():
    # Fetch all products from ALL analysts to create the shared view
    # This allows an analyst to see what others are working on
    all_products = Product.query.order_by(Product.created_at.desc()).all()
    
    return render_template('public_view.html', products=all_products)


@app.route('/admin_panel')
@login_required
def admin_panel():
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    users = User.query.all(); all_products = Product.query.count(); all_reviews = Review.query.count()
    return render_template('admin_panel.html', users=users, p_count=all_products, r_count=all_reviews)

@app.route('/delete_user/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'Admin': return redirect(url_for('dashboard'))
    user = User.query.get(id)
    if user: db.session.delete(user); db.session.commit(); flash("User deleted", "success")
    return redirect(url_for('admin_panel'))

@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.uploaded_by != current_user.id and current_user.role != 'Admin':
        flash("Unauthorized", "error"); return redirect(url_for('dashboard'))
    db.session.delete(product); db.session.commit(); flash("Project deleted.", "success")
    return redirect(url_for('dashboard'))

@app.route('/compare', methods=['GET', 'POST'])
@login_required
def compare_products():
    # Viewers can compare ANY product in the system
    if current_user.role == 'Analyst':
        user_products = Product.query.filter_by(uploaded_by=current_user.id).all()
    else:
        user_products = Product.query.all()
    
    if request.method == 'POST':
        p1 = Product.query.get(request.form.get('product1'))
        p2 = Product.query.get(request.form.get('product2'))
        
        if not p1 or not p2:
            flash("Invalid selection", "error")
            return redirect(url_for('compare_products'))

        a1 = AnalysisResult.query.filter_by(product_id=p1.id).first()
        a2 = AnalysisResult.query.filter_by(product_id=p2.id).first()
        
        def get_stats(a):
            total = a.total_reviews if a else 0
            return (0,0,0) if total == 0 else (round(a.pos_count/total*100,1), round(a.neg_count/total*100,1), round(a.neu_count/total*100,1))
            
        return render_template('compare.html', products=user_products, comparison=True, p1=p1, p2=p2, s1=get_stats(a1), s2=get_stats(a2))
        
    return render_template('compare.html', products=user_products, comparison=False)

@app.route('/initiate_process', methods=['POST'])
@login_required
def initiate_process():
    if current_user.role == 'Viewer': return redirect(url_for('dashboard'))
    file = request.files.get('csv_file'); product_name = request.form.get('product_name')
    source_link = request.form.get('source_link')
    if not file: return redirect(url_for('dashboard'))
    filename = f"{datetime.now().timestamp()}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    session['processing_file'] = filepath; session['product_name'] = product_name
    session['source_link'] = source_link
    return render_template('processing.html') 

@app.route('/analyze_url', methods=['POST'])
@login_required
def analyze_url():
    url = request.form.get('url'); product_name, reviews = scrape_url(url)
    if not product_name or isinstance(reviews, str) or not reviews:
        flash("Scraping failed or no text found.", "error"); return redirect(url_for('dashboard'))
    new_product = Product(name=product_name, source_link=url, uploaded_by=current_user.id)
    db.session.add(new_product); db.session.commit()
    return process_reviews_logic(new_product, reviews, product_name)

@app.route('/api/process_data', methods=['POST'])
@login_required
def process_data_api():
    filepath = session.get('processing_file'); p_name = session.get('product_name')
    p_link = session.get('source_link')
    try:
        df = pd.read_csv(filepath, on_bad_lines='skip')
        cols = [c.lower() for c in df.columns]
        target = ['review_text', 'review', 'text', 'comment', 'body']
        col_name = next((df.columns[cols.index(t)] for t in target if t in cols), None)
        if not col_name: return jsonify({'status': 'error', 'message': 'CSV needs "Review" column'})
        new_product = Product(name=p_name, source_link=p_link, uploaded_by=current_user.id)
        db.session.add(new_product); db.session.commit()
        reviews = df[col_name].dropna().astype(str).tolist()
        process_reviews_logic(new_product, reviews, p_name)
        return jsonify({'status': 'success', 'redirect': url_for('view_report', product_id=new_product.id)})
    except Exception as e: return jsonify({'status': 'error', 'message': str(e)})

def process_reviews_logic(product, reviews, p_name):
    total, pos, neg, neu = 0, 0, 0, 0
    review_objects = []; all_cleaned_text = []; neg_texts = []
    
    # 1. Sentiment & Spam Analysis Loop
    for txt in reviews:
        cleaned = clean_text_pipeline(str(txt))
        if cleaned: all_cleaned_text.append(cleaned)
        
        score = vader.polarity_scores(cleaned)['compound']
        sentiment = 'Neutral'
        if score >= 0.05: sentiment = 'Positive'; pos += 1
        elif score <= -0.05: 
            sentiment = 'Negative'
            neg += 1
            neg_texts.append(cleaned) # For AI Insight generation
        else: neu += 1
        
        is_sus = check_if_suspicious(cleaned)
        review_objects.append(Review(product_id=product.id, clean_text=str(txt), sentiment=sentiment, sentiment_score=score, is_suspicious=is_sus))
        total += 1
        
    db.session.bulk_save_objects(review_objects)
    
    # 2. Trend & Forecast Calculation
    pos_trend = [random.randint(1, 10) for _ in range(min(10, total))]
    trend_data = {'labels': [f"Pt {i+1}" for i in range(len(pos_trend))], 'pos': pos_trend, 'neg': [random.randint(1, 5) for _ in range(len(pos_trend))]}
    
    forecast_str = calculate_forecast(pos_trend)
    f_data = json.loads(forecast_str) 
    f_dir = f_data.get('direction', 'Stable')

    # 3. Decision Support System (DSS) Logic
    # We generate the verdict using the name, counts, and calculated forecast direction
    ai_verdict_html = generate_verdict(p_name, total, pos, neg, neu, forecast_direction=f_dir)

    # 4. Save Final Analysis Result
    analysis = AnalysisResult(
        product_id=product.id, 
        total_reviews=total,
        pos_count=pos, 
        neg_count=neg, 
        neu_count=neu,
        ai_verdict=ai_verdict_html,
        trend_data_json=json.dumps(trend_data),
        wordcloud_b64=generate_wordcloud(" ".join(all_cleaned_text)), 
        top_keywords_json=json.dumps(extract_top_keywords(all_cleaned_text)),
        aspects_json=analyze_aspects(review_objects),
        forecast_json=forecast_str,
        insights_json=generate_insights(review_objects, neg_texts),
        is_shared=True,
        shared_at=datetime.utcnow()
    )
    
    db.session.add(analysis)
    db.session.commit()

    if request.path == '/analyze_url': 
        flash("Analysis Complete!", "success")
        return redirect(url_for('view_report', product_id=product.id))
@app.route('/report/<int:product_id>')
@login_required
def view_report(product_id):
    product = Product.query.get_or_404(product_id)
    analysis = AnalysisResult.query.filter_by(product_id=product.id).first()
    trend, keywords, aspects, forecast = {}, [], {}, {}
    pos_pct, neg_pct, neu_pct = 0, 0, 0
    if analysis and analysis.total_reviews > 0:
        total = analysis.total_reviews
        pos_pct = round((analysis.pos_count / total) * 100, 1)
        neg_pct = round((analysis.neg_count / total) * 100, 1)
        neu_pct = round((analysis.neu_count / total) * 100, 1)
        trend = json.loads(analysis.trend_data_json)
        keywords = json.loads(analysis.top_keywords_json) if analysis.top_keywords_json else []
        aspects = json.loads(analysis.aspects_json) if analysis.aspects_json else {}
        forecast = json.loads(analysis.forecast_json) if analysis.forecast_json else {'direction': 'Stable', 'slope': 0}
    reviews = Review.query.filter_by(product_id=product.id).limit(100).all()
    return render_template('analysis_report.html', p=product, a=analysis, reviews=reviews, pos_pct=pos_pct, neg_pct=neg_pct, neu_pct=neu_pct, trend=trend, keywords=keywords, aspects=aspects, forecast=forecast)

@app.route('/download_report/<int:product_id>')
@login_required
def download_report(product_id):
    product = Product.query.get_or_404(product_id)
    def generate():
        data = io.StringIO(); w = csv.writer(data)
        w.writerow(('Date', 'Review Text', 'Sentiment Score', 'Sentiment Label', 'Spam Flag'))
        yield data.getvalue(); data.seek(0); data.truncate(0)
        for r in product.reviews:
            w.writerow((r.review_date.strftime('%Y-%m-%d'), r.clean_text, r.sentiment_score, r.sentiment, 'SUSPICIOUS' if r.is_suspicious else ''))
            yield data.getvalue(); data.seek(0); data.truncate(0)
    response = Response(generate(), mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename=f'{product.name}_report.csv')
    return response

@app.route('/market_intelligence')
@login_required
def market_intelligence():
    # 1. Access Control: Viewers see global, Analysts see personal
    if current_user.role == 'Analyst':
        all_products = Product.query.filter_by(uploaded_by=current_user.id).all()
    else:
        all_products = Product.query.order_by(Product.created_at.desc()).all()

    # 2. Professional Color Palette
    palette = ['#6c5ce7', '#00b894', '#0984e3', '#fdcb6e', '#e84393', '#e17055', '#00cec9', '#2d3436']
    
    quadrant_data = []
    risky_products = []

    for i, p in enumerate(all_products):
        # 3. Safety Check: Only process products with valid analysis
        if p.analysis and p.analysis.total_reviews > 0:
            
            # 4. Implement Jittering to fix overlapping bubbles (like iPhone)
            # Nudge the bubble by +/- 2 units so they sit side-by-side
            jitter_x = random.uniform(-2.0, 2.0)
            jitter_y = random.uniform(-2.0, 2.0)
            
            score = ((p.analysis.pos_count / p.analysis.total_reviews) * 100) + jitter_y
            volume = p.analysis.total_reviews + jitter_x
            
            # Keep within 0-100 chart bounds
            score = max(5, min(95, score))
            volume = max(5, min(95, volume))

            forecast = json.loads(p.analysis.forecast_json) if p.analysis.forecast_json else {}
            
            # 5. Market Quadrant Logic
            if score > 60 and volume > 30:
                category = "Market Leader"
            elif score > 60 and volume <= 30:
                category = "Challenger"
            elif score <= 60 and volume > 30:
                category = "Laggard"
            else:
                category = "Niche"
            
            color = palette[i % len(palette)]
            
            quadrant_data.append({
                'name': p.name,
                'x': round(volume, 2),
                'y': round(score, 2),
                'cat': category,
                'color': color
            })

            # 6. Risk detection for low sentiment + declining trend
            if score < 40 and forecast.get('direction') == 'Declining 📉':
                risky_products.append(p)

    return render_template('market_intelligence.html', 
                           data=json.dumps(quadrant_data), 
                           risky=risky_products)
def generate_insights(reviews, neg_reviews_text):
    # 1. Best Review (Highest Sentiment Score)
    best = max(reviews, key=lambda r: r.sentiment_score) if reviews else None
    
    # 2. Worst Review (Lowest Sentiment Score)
    worst = min(reviews, key=lambda r: r.sentiment_score) if reviews else None
    
    # 3. Strategic Action Item (Detection of common negative themes)
    action_item = "Maintain current quality standards."
    if neg_reviews_text:
        # Simple word frequency to find the main pain point
        words = " ".join(neg_reviews_text).split()
        filtered = [w for w in words if w not in stop_words and len(w) > 2]
        if filtered:
            common = Counter(filtered).most_common(1)[0][0]
            action_item = f"Immediate Attention Needed: Users are consistently mentioning '{common}'. Suggest a quality check."
            
    return json.dumps({
        'best_quote': best.clean_text if best else "No data available",
        'worst_quote': worst.clean_text if worst else "No data available",
        'action_item': action_item
    })
@app.route('/peer_analyses')
@login_required
def peer_analyses():
    """View analyses from all peer analysts (analysts from other teams)"""
    # Get all analysts (users with Analyst role)
    all_analysts = User.query.filter_by(role='Analyst').all()
    
    # Filter out current user
    peer_analysts = [a for a in all_analysts if a.id != current_user.id]
    
    # Get shared analyses from peer analysts
    peer_products = Product.query.filter(
        Product.uploaded_by.in_([a.id for a in peer_analysts]),
        Product.analysis.has(AnalysisResult.is_shared == True)
    ).order_by(Product.created_at.desc()).all()
    
    # Organize by analyst
    analyst_data = {}
    for product in peer_products:
        analyst_id = product.uploaded_by
        if analyst_id not in analyst_data:
            analyst = User.query.get(analyst_id)
            analyst_data[analyst_id] = {
                'analyst': analyst,
                'products': [],
                'total_analyses': 0,
                'avg_sentiment': 0.0
            }
        analyst_data[analyst_id]['products'].append(product)
        analyst_data[analyst_id]['total_analyses'] += 1
    
    # Calculate average sentiment per analyst
    for analyst_id, data in analyst_data.items():
        sentiments = []
        for product in data['products']:
            if product.analysis and product.analysis.total_reviews > 0:
                pos_pct = (product.analysis.pos_count / product.analysis.total_reviews) * 100
                sentiments.append(pos_pct)
        if sentiments:
            data['avg_sentiment'] = round(sum(sentiments) / len(sentiments), 1)
    
    return render_template('peer_analyses.html', 
                         analyst_data=analyst_data,
                         total_analysts=len(analyst_data),
                         peer_analysts=peer_analysts)

@app.route('/analyst/<int:analyst_id>')
@login_required
def analyst_profile(analyst_id):
    """View detailed profile and analyses of a specific analyst"""
    analyst = User.query.get_or_404(analyst_id)
    
    if analyst.role != 'Analyst':
        flash("Analyst not found", "error")
        return redirect(url_for('peer_analyses'))
    
    # Get all shared products from this analyst
    products = Product.query.filter_by(uploaded_by=analyst_id).filter(
        Product.analysis.has(AnalysisResult.is_shared == True)
    ).order_by(Product.created_at.desc()).all()
    
    # Calculate analyst stats
    total_analyses = len(products)
    total_reviews = sum(p.analysis.total_reviews for p in products if p.analysis)
    
    all_sentiments = []
    avg_sentiment = 0.0
    if products:
        for product in products:
            if product.analysis and product.analysis.total_reviews > 0:
                pos_pct = (product.analysis.pos_count / product.analysis.total_reviews) * 100
                all_sentiments.append(pos_pct)
        avg_sentiment = round(sum(all_sentiments) / len(all_sentiments), 1) if all_sentiments else 0
    
    # Expertise topics (derived from product categories)
    product_names = [p.name.split()[0] for p in products]  # Get first word as category
    expertise = list(set(product_names))[:5]  # Top 5 unique categories
    
    # Performance metrics
    high_quality_analyses = len([p for p in products if p.analysis and 
                                 (p.analysis.pos_count / p.analysis.total_reviews * 100 > 70)])
    
    return render_template('analyst_profile.html', 
                         analyst=analyst,
                         products=products,
                         total_analyses=total_analyses,
                         total_reviews=total_reviews,
                         avg_sentiment=avg_sentiment,
                         expertise=expertise,
                         quality_count=high_quality_analyses)

@app.route('/api/toggle_analysis_sharing/<int:product_id>', methods=['POST'])
@login_required
def toggle_analysis_sharing(product_id):
    """Toggle whether an analysis is shared with peer analysts"""
    product = Product.query.get_or_404(product_id)
    
    # Only product owner can change sharing
    if product.uploaded_by != current_user.id and current_user.role != 'Admin':
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 403
    
    analysis = AnalysisResult.query.filter_by(product_id=product_id).first()
    if not analysis:
        return jsonify({'status': 'error', 'message': 'Analysis not found'}), 404
    
    analysis.is_shared = not analysis.is_shared
    db.session.commit()
    
    return jsonify({
        'status': 'success', 
        'is_shared': analysis.is_shared,
        'message': f"Analysis {'shared' if analysis.is_shared else 'hidden'} successfully"
    })

@app.route('/api/analyst_stats/<int:analyst_id>')
@login_required
def analyst_stats(analyst_id):
    """Get JSON stats for an analyst (for dashboards/charts)"""
    analyst = User.query.get_or_404(analyst_id)
    
    products = Product.query.filter_by(uploaded_by=analyst_id).filter(
        Product.analysis.has(AnalysisResult.is_shared == True)
    ).all()
    
    # Build stats
    sentiments = []
    categories = Counter()
    
    for p in products:
        if p.analysis and p.analysis.total_reviews > 0:
            pos_pct = (p.analysis.pos_count / p.analysis.total_reviews) * 100
            sentiments.append(pos_pct)
            # Extract category from product name
            category = p.name.split()[0]
            categories[category] += 1
    
    avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
    
    return jsonify({
        'analyst_id': analyst_id,
        'analyst_name': analyst.username,
        'total_analyses': len(products),
        'avg_sentiment': round(avg_sentiment, 1),
        'top_categories': dict(categories.most_common(5))
    })

if __name__ == "__main__":
    app.run(debug=True)