# 🧠 Product Review Analyzer

An AI-powered sentiment analysis platform that classifies customer reviews as Positive, Negative, or Neutral using an ensemble NLP approach (VADER + TextBlob), achieving **95%+ accuracy** across 1,000+ reviews.

Built as a final year BSc IT project at Usha Pravin Gandhi College of Arts, Science and Commerce.

---

## 🚀 Features

- **Sentiment Analysis** — Ensemble VADER + TextBlob classification with 95%+ accuracy
- **Aspect-Based Analysis** — Extracts customer sentiment for Quality, Price, Performance, and Service
- **Multilingual Support** — Auto-detects and translates reviews in 17+ languages to English
- **Spam Detection** — Flags bot-generated, repetitive, or suspicious reviews
- **Trend Forecasting** — Linear regression-based sentiment trend prediction
- **Interactive Dashboard** — Word clouds, pie charts, trend graphs, and market intelligence bubble charts
- **PDF & CSV Export** — Auto-generates downloadable analysis reports
- **Role-Based Access** — Admin, Analyst, and Viewer roles with OTP email verification
- **Email Alerts** — Automatic notifications when sentiment drops below threshold
- **Peer Collaboration** — Share analyses with other analysts

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python, Flask |
| NLP | VADER, TextBlob, NLTK |
| Frontend | HTML5, CSS3, JavaScript, Bootstrap, Chart.js |
| Database | SQLite (SQLAlchemy ORM) |
| Data Processing | Pandas, NumPy |
| Multilingual | langdetect, deep-translator |
| Visualization | Matplotlib, WordCloud, ReportLab |
| Auth | Flask-Login, OTP via SMTP |

---

## 📊 Performance

- Processes **10,000+ reviews in under 2 minutes** using parallel processing
- Sentiment classification accuracy: **95%+**
- Supports datasets up to **1,000,000 reviews**
- Tested across **40 test cases** — all passed

---

## 🖥️ Screenshots

> Dashboard showing sentiment distribution, word cloud, aspect breakdown, and trend analysis.

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.8+
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Palak985/Product_Analyzer.git
cd Product_Analyzer

# 2. Create a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python app.py
```

Then open your browser and go to: `http://localhost:5000`

---

## 📁 Project Structure

```
product-review-analyzer/
├── app.py                  # Main Flask application
├── models.py               # Database models
├── model_utils.py          # Sentiment analysis engine
├── enhanced_sentiment_analyzer.py
├── analytics/              # Advanced analytics module
├── blueprints/             # Flask blueprints
├── services/               # Recommendation engine
├── utils/                  # Language processor, spam detector
├── templates/              # HTML templates
├── static/                 # CSS and assets
├── requirements.txt
└── README.md
```

---

## 📂 Input Format

Upload a CSV file with the following columns (flexible detection):

| Column | Description |
|--------|-------------|
| `review_text` | Customer review content |
| `rating` | Numeric rating (1–5) |
| `date` | Review date (optional) |

Sample datasets included: `iphone_14_reviews.csv`, `samsung_galaxy_s24_reviews.csv`, etc.

---

## 👤 User Roles

| Role | Access |
|------|--------|
| Admin | User management, audit logs, system config |
| Analyst | Upload reviews, run analysis, generate reports, share |
| Viewer | Read-only access to shared analyses |

---

## 📈 Key Modules

- **Sentiment Engine** — VADER + TextBlob ensemble with confidence scoring
- **Aspect Extractor** — Keyword-level analysis for Quality, Price, Performance, Service
- **Spam Detector** — Lexical diversity and repetition pattern detection
- **Trend Analyzer** — Linear regression forecasting for sentiment direction
- **Report Generator** — PDF reports with charts, word clouds, and recommendations

---

## 🎓 Academic Context

- **Degree:** BSc Information Technology (TY)
- **College:** Usha Pravin Gandhi College of Arts, Science and Commerce, Mumbai
- **Project Type:** Final Year Project (Black Book)
- **Domain:** NLP, Sentiment Analysis, Full-Stack Web Development

---

## 👩‍💻 Developer

**Palak Santoki**
- 📧 [LinkedIn](https://www.linkedin.com/in/palak-santoki-825442318)
- 💻 [GitHub](https://github.com/Palak985)
- 🎓 Currently pursuing Data Science (AI) 2.0 with Data Analytics — Try Catch Classes

---

## 📄 License

This project is for educational purposes. Feel free to fork and build on it.
