# EduPro: Learner Demographics & Course Enrollment Behavior Analysis

Starter kit for the project. Contains everything needed to run the EDA in
**Google Colab** and the dashboard in **Streamlit**.

## Files
| File | Purpose |
|---|---|
| `generate_sample_data.py` | Creates synthetic `users.csv`, `courses.csv`, `transactions.csv` matching the project schema. Use this until you have EduPro's real data. |
| `users.csv`, `courses.csv`, `transactions.csv` | Sample data (1,200 users / 120 courses / 6,000 enrollments). Replace with real EduPro exports — just keep the same column names. |
| `EduPro_Analysis.ipynb` | The Colab notebook: data integration, demographic analysis, enrollment distribution, heatmaps, KPIs, and auto-drafted insight bullets for your research paper. |
| `app.py` | The Streamlit dashboard: filters + 4 tabs (Demographics, Age-wise Enrollment, Gender Preferences, Category Popularity). |
| `requirements.txt` | Python packages needed. |

---

## Part 1 — Running the analysis in Google Colab

1. Go to https://colab.research.google.com → **File → Upload notebook** → upload `EduPro_Analysis.ipynb`.
2. In the Colab file sidebar (folder icon on the left), click **Upload** and add `users.csv`, `courses.csv`, `transactions.csv`.
   - Alternative: if your data lives in Google Drive, use the "mount Google Drive" cell at the top of the notebook instead, and change the `pd.read_csv(...)` paths to point at your Drive folder.
3. Run cells top to bottom (**Runtime → Run all**, or step through with Shift+Enter).
4. Each section produces a chart plus printed numbers — these map directly onto the project's required analyses:
   - Section 1: data integration + referential integrity checks
   - Section 2: age distribution, gender distribution
   - Section 3: enrollments by category / type / level
   - Section 4: age-group × category heatmap, gender × level comparison
   - Section 5: avg courses per learner, enrollment concentration, beginner vs advanced patterns
   - Section 6: KPI summary table
   - Section 7: auto-drafted insight sentences — edit these into your research paper's findings section
5. To swap in real data: just re-upload the three CSVs with the same column names (`UserID`, `Age`, `Gender`, `CourseID`, `CourseCategory`, `CourseType`, `CourseLevel`, `TransactionID`, `TransactionDate`) and re-run.

**For your research paper:** copy each chart (right-click → "Save image as") and the printed KPI/insight text into your document, then write the "so what" — e.g., why does the 18–25 group dominating Programming enrollments matter for course planning?

---

## Part 2 — Running the Streamlit dashboard

### Option A: Run locally (recommended)
```bash
# 1. Create a folder and put app.py, users.csv, courses.csv, transactions.csv,
#    requirements.txt all in it

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```
This opens the dashboard at `http://localhost:8501` in your browser.

### Option B: Run from Google Colab (works, but clunky)
Colab doesn't serve web apps directly, so you need a tunnel. In a Colab cell:
```python
!pip install streamlit -q
!wget -q -O - ipv4.icanhazip.com   # note this IP, you'll paste it into the tunnel page

!npm install -g localtunnel
!streamlit run app.py &>/content/logs.txt &
!npx localtunnel --port 8501
```
Click the URL localtunnel prints, then enter the IP address from the `wget` step when prompted. This works for quick demos but is not reliable for a submitted deliverable — **use Option A or C for anything you're actually handing in.**

### Option C: Deploy for free so it's a live link (best for submission)
1. Push this folder to a GitHub repository (include `app.py`, the 3 CSVs, `requirements.txt`).
2. Go to https://share.streamlit.io → sign in with GitHub → "New app".
3. Point it at your repo and `app.py`. Click Deploy.
4. You get a public URL (e.g. `https://your-app.streamlit.app`) — this is what you submit/link in your executive summary as the "live analytics" deliverable.

---

## What the dashboard gives you (mapped to the project's requirements)
- **Sidebar filters:** Age Group, Gender, Course Category, Course Level — all combine (AND logic).
- **KPI row:** Total Enrollments, Unique Learners, Courses Offered, Avg Enrollments/Learner, Top Category.
- **Tab 1 – Learner Demographics:** age histogram, gender pie chart, age×gender participation table.
- **Tab 2 – Age-wise Enrollment:** enrollments by age group, age×category heatmap, age×level stacked bars.
- **Tab 3 – Gender-based Preferences:** gender×category heatmap, gender×level stacked bars, gender×type table.
- **Tab 4 – Category Popularity:** category popularity bar chart, course type pie, level distribution pie.
- **Footer:** auto-computed behavioral insights (avg courses/learner, enrollment concentration, top category/level) that update live as filters change.

## Swapping in real EduPro data
Replace the three CSVs, keeping these exact column names:
- `users.csv`: `UserID, UserName, Age, Gender`
- `courses.csv`: `CourseID, CourseName, CourseCategory, CourseType, CourseLevel`
- `transactions.csv`: `TransactionID, UserID, CourseID, TransactionDate`

If your real data is in Excel instead of CSV, either export each sheet to CSV, or change the three `pd.read_csv(...)` lines in `app.py` / the notebook to `pd.read_excel("EduProData.xlsx", sheet_name="Users")` etc.

## Suggested next steps for the full deliverable set
1. Finish the EDA in Colab, save all charts + narrative → **research paper**.
2. Deploy `app.py` via Streamlit Community Cloud → **live dashboard**.
3. Condense the KPI table + top 5 insight bullets from the notebook into one page → **executive summary** for stakeholders (lead with numbers, keep language non-technical).
