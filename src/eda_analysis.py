import io
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Pfade
DATA_PATH = Path("data/raw/mental-health-in-tech-2016_20161114.csv")
FIGURES_DIR = Path("documentation/eda_figures")
REPORT_PATH = Path("documentation/eda_report.md")

FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Darstellungsoptionen
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', 80)
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100
sns.set_style('whitegrid')

report_lines = []

def h(text, level=2):
    report_lines.append(f"{'#' * level} {text}")

def p(text):
    report_lines.append(str(text))

def fig(filename, caption=""):
    rel = f"eda_figures/{filename}"
    report_lines.append(f"![{caption}]({rel})")


# -----------------------------------------------------------------------
# 1. Import
# -----------------------------------------------------------------------
df = pd.read_csv(DATA_PATH)
print(f"Datensatz geladen: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")

# -----------------------------------------------------------------------
# 2. Spaltennamen kürzen
# -----------------------------------------------------------------------
COLUMN_ALIASES = {
    "Are you self-employed?": "self_employed",
    "How many employees does your company or organization have?": "company_size",
    "Is your employer primarily a tech company/organization?": "tech_company",
    "Is your primary role within your company related to tech/IT?": "tech_role",
    "Does your employer provide mental health benefits as part of healthcare coverage?": "mh_benefits",
    "Do you know the options for mental health care available under your employer-provided coverage?": "know_options",
    "Has your employer ever formally discussed mental health (for example, as part of a wellness campaign or other official communication)?": "employer_discussed_mh",
    "Does your employer offer resources to learn more about mental health concerns and options for seeking help?": "employer_resources",
    "Is your anonymity protected if you choose to take advantage of mental health or substance abuse treatment resources provided by your employer?": "anonymity_protected",
    "If a mental health issue prompted you to request a medical leave from work, asking for that leave would be:": "leave_difficulty",
    "Do you think that discussing a mental health disorder with your employer would have negative consequences?": "neg_consequences_employer",
    "Do you think that discussing a physical health issue with your employer would have negative consequences?": "neg_consequences_physical",
    "Would you feel comfortable discussing a mental health disorder with your coworkers?": "comfortable_coworkers",
    "Would you feel comfortable discussing a mental health disorder with your direct supervisor(s)?": "comfortable_supervisor",
    "Do you feel that your employer takes mental health as seriously as physical health?": "employer_takes_mh_serious",
    "Have you heard of or observed negative consequences for co-workers who have been open about mental health issues in your workplace?": "observed_neg_consequences",
    "Do you have medical coverage (private insurance or state-provided) which includes treatment of \xa0mental health issues?": "medical_coverage",
    "Do you know local or online resources to seek help for a mental health disorder?": "know_resources",
    "If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to clients or business contacts?": "reveal_clients",
    "If you have revealed a mental health issue to a client or business contact, do you believe this has impacted you negatively?": "reveal_clients_impact",
    "If you have been diagnosed or treated for a mental health disorder, do you ever reveal this to coworkers or employees?": "reveal_coworkers",
    "If you have revealed a mental health issue to a coworker or employee, do you believe this has impacted you negatively?": "reveal_coworkers_impact",
    "Do you believe your productivity is ever affected by a mental health issue?": "productivity_affected",
    "If yes, what percentage of your work time (time performing primary or secondary job functions) is affected by a mental health issue?": "pct_work_affected",
    "Do you have previous employers?": "has_previous_employers",
    "Have your previous employers provided mental health benefits?": "prev_mh_benefits",
    "Were you aware of the options for mental health care provided by your previous employers?": "prev_aware_options",
    "Did your previous employers ever formally discuss mental health (as part of a wellness campaign or other official communication)?": "prev_discussed_mh",
    "Did your previous employers provide resources to learn more about mental health issues and how to seek help?": "prev_resources",
    "Was your anonymity protected if you chose to take advantage of mental health or substance abuse treatment resources with previous employers?": "prev_anonymity",
    "Do you think that discussing a mental health disorder with previous employers would have negative consequences?": "prev_neg_consequences",
    "Do you think that discussing a physical health issue with previous employers would have negative consequences?": "prev_neg_physical",
    "Would you have been willing to discuss a mental health issue with your previous co-workers?": "prev_comfortable_coworkers",
    "Would you have been willing to discuss a mental health issue with your direct supervisor(s)?": "prev_comfortable_supervisor",
    "Did you feel that your previous employers took mental health as seriously as physical health?": "prev_mh_serious",
    "Did you hear of or observe negative consequences for co-workers with mental health issues in your previous workplaces?": "prev_observed_neg",
    "Would you be willing to bring up a physical health issue with a potential employer in an interview?": "interview_physical",
    "Why or why not?": "interview_physical_why",
    "Would you bring up a mental health issue with a potential employer in an interview?": "interview_mental",
    "Do you feel that being identified as a person with a mental health issue would hurt your career?": "mh_hurts_career",
    "Do you think that team members/co-workers would view you more negatively if they knew you suffered from a mental health issue?": "coworkers_view_neg",
    "How willing would you be to share with friends and family that you have a mental illness?": "share_friends_family",
    "Have you observed or experienced an unsupportive or badly handled response to a mental health issue in your current or previous workplace?": "observed_bad_response",
    "Have your observations of how another individual who discussed a mental health disorder made you less likely to reveal a mental health issue yourself in your current workplace?": "observations_less_likely",
    "Do you have a family history of mental illness?": "family_history",
    "Have you had a mental health disorder in the past?": "past_disorder",
    "Do you currently have a mental health disorder?": "current_disorder",
    "If yes, what condition(s) have you been diagnosed with?": "diagnosed_conditions",
    "If maybe, what condition(s) do you believe you have?": "believed_conditions",
    "Have you been diagnosed with a mental health condition by a medical professional?": "professionally_diagnosed",
    "If so, what condition(s) were you diagnosed with?": "professional_diagnosis_detail",
    "Have you ever sought treatment for a mental health issue from a mental health professional?": "sought_treatment",
    "If you have a mental health issue, do you feel that it interferes with your work when being treated effectively?": "interferes_treated",
    "If you have a mental health issue, do you feel that it interferes with your work when NOT being treated effectively?": "interferes_untreated",
    "What is your age?": "age",
    "What is your gender?": "gender",
    "What country do you live in?": "country_live",
    "What US state or territory do you live in?": "us_state_live",
    "What country do you work in?": "country_work",
    "What US state or territory do you work in?": "us_state_work",
    "Which of the following best describes your work position?": "work_position",
    "Do you work remotely?": "remote_work",
}

rename_map = {k: v for k, v in COLUMN_ALIASES.items() if k in df.columns}
df.rename(columns=rename_map, inplace=True)

if "Why or why not?.1" in df.columns:
    df.rename(columns={"Why or why not?.1": "interview_mental_why"}, inplace=True)

# -----------------------------------------------------------------------
# 3. Datenstruktur
# -----------------------------------------------------------------------
h("Datenstruktur", 2)
p(f"**Zeilen:** {df.shape[0]}  \n**Spalten:** {df.shape[1]}")
p("```")
buf = io.StringIO()
df.info(buf=buf)
p(buf.getvalue())
p("```")

# -----------------------------------------------------------------------
# 4. Fehlende Werte
# -----------------------------------------------------------------------
missing = df.isnull().sum()
missing_pct = (missing / len(df) * 100).round(1)
missing_df = pd.DataFrame({
    'Fehlend': missing,
    'Prozent': missing_pct
}).sort_values('Fehlend', ascending=False)

missing_plot = missing_df[missing_df['Fehlend'] > 0].sort_values('Fehlend', ascending=True)

fig_mv, ax_mv = plt.subplots(figsize=(10, max(6, len(missing_plot) * 0.3)))
ax_mv.barh(range(len(missing_plot)), missing_plot['Prozent'], color='steelblue', alpha=0.7)
ax_mv.set_yticks(range(len(missing_plot)))
ax_mv.set_yticklabels(missing_plot.index, fontsize=8)
ax_mv.set_xlabel('Fehlende Werte (%)')
ax_mv.set_title('Fehlende Werte pro Spalte')
plt.tight_layout()
plt.savefig(FIGURES_DIR / "missing_values.png")
plt.close()

n_self_employed = (df['self_employed'] == 1).sum()
n_missing_company_size = df['company_size'].isnull().sum()

h("Fehlende Werte", 2)
p("| Spalte | Fehlend | Prozent |")
p("|--------|---------|---------|")
for col, row in missing_df[missing_df['Fehlend'] > 0].iterrows():
    p(f"| {col} | {int(row['Fehlend'])} | {row['Prozent']}% |")
p(f"\nSelbstständige: {n_self_employed} | Fehlende Werte bei `company_size`: {n_missing_company_size} | Übereinstimmung: {n_self_employed == n_missing_company_size}")
fig("missing_values.png", "Fehlende Werte pro Spalte")

# -----------------------------------------------------------------------
# 5. Datentypen
# -----------------------------------------------------------------------
h("Datentypen", 2)
p("```")
p(str(df.dtypes.value_counts()))
p(f"\nGesamtzahl Spalten: {len(df.columns)}")
p("```")

# -----------------------------------------------------------------------
# 6. Alter
# -----------------------------------------------------------------------
outliers = df[(df['age'] < 18) | (df['age'] > 80)]
ages_clean = df['age'][(df['age'] >= 18) & (df['age'] <= 80)]

fig_age, axes_age = plt.subplots(1, 2, figsize=(14, 5))

axes_age[0].hist(df['age'].dropna(), bins=50, color='steelblue', edgecolor='black', alpha=0.7)
axes_age[0].set_xlabel('Alter')
axes_age[0].set_ylabel('Anzahl')
axes_age[0].set_title('Altersverteilung (alle Werte)')

axes_age[1].hist(ages_clean, bins=30, color='steelblue', edgecolor='black', alpha=0.7)
axes_age[1].set_xlabel('Alter')
axes_age[1].set_ylabel('Anzahl')
axes_age[1].set_title('Altersverteilung (bereinigt, 18-80)')
axes_age[1].axvline(ages_clean.mean(), color='red', linestyle='--', label=f'Mittelwert: {ages_clean.mean():.1f}')
axes_age[1].axvline(ages_clean.median(), color='orange', linestyle='--', label=f'Median: {ages_clean.median():.0f}')
axes_age[1].legend()

plt.tight_layout()
plt.savefig(FIGURES_DIR / "dist_age.png")
plt.close()

h("Alter", 2)
age_desc = df['age'].describe()
p("| | Wert |")
p("|--|------|")
for idx, val in age_desc.items():
    p(f"| {idx} | {val:.2f} |")
p(f"\nAusreißer (< 18 oder > 80): {len(outliers)} | Werte: {sorted(int(x) for x in outliers['age'].unique())}")
fig("dist_age.png", "Altersverteilung")

# -----------------------------------------------------------------------
# 7. Gender
# -----------------------------------------------------------------------
fig_gender, ax_gender = plt.subplots(figsize=(10, 6))
top_gender = df['gender'].value_counts().head(15)
ax_gender.barh(range(len(top_gender)), top_gender.values, color='coral', alpha=0.7)
ax_gender.set_yticks(range(len(top_gender)))
ax_gender.set_yticklabels(top_gender.index)
ax_gender.set_xlabel('Anzahl')
ax_gender.set_title('Verteilung Gender-Werte (Top 15)')
ax_gender.invert_yaxis()
plt.tight_layout()
plt.savefig(FIGURES_DIR / "dist_gender.png")
plt.close()

h("Gender", 2)
p(f"Unique Rohwerte: {df['gender'].nunique()} | Fehlende Werte: {df['gender'].isnull().sum()}")
fig("dist_gender.png", "Gender-Verteilung (Top 15)")

# -----------------------------------------------------------------------
# 8. Geographische Verteilung
# -----------------------------------------------------------------------
fig_country, ax_country = plt.subplots(figsize=(10, 6))
countries = df['country_live'].value_counts().head(15)
ax_country.barh(range(len(countries)), countries.values, color='steelblue', alpha=0.7)
ax_country.set_yticks(range(len(countries)))
ax_country.set_yticklabels(countries.index)
ax_country.set_xlabel('Anzahl')
ax_country.set_title('Top 15 Länder (Wohnort)')
ax_country.invert_yaxis()
plt.tight_layout()
plt.savefig(FIGURES_DIR / "dist_country_live.png")
plt.close()

h("Geographische Verteilung", 2)
p(f"Verschiedene Länder: {df['country_live'].nunique()} | Anteil USA: {(df['country_live'] == 'United States of America').sum() / len(df) * 100:.1f}%")
fig("dist_country_live.png", "Top 15 Länder (Wohnort)")

# -----------------------------------------------------------------------
# 9. Aktuelle Störung vs. Behandlung gesucht
# -----------------------------------------------------------------------
ct = pd.crosstab(df['current_disorder'], df['sought_treatment'], margins=True)

h("Aktuelle MH-Störung vs. Behandlung gesucht", 2)
cols = ct.columns.tolist()
p("| | " + " | ".join(str(c) for c in cols) + " |")
p("|--" + "|--" * len(cols) + "|")
for idx, row in ct.iterrows():
    p("| " + str(idx) + " | " + " | ".join(str(row[c]) for c in cols) + " |")

# -----------------------------------------------------------------------
# 10. Negative Konsequenzen bei Gespräch mit AG
# -----------------------------------------------------------------------
fig_neg, axes_neg = plt.subplots(1, 2, figsize=(14, 5))

for i, (col, title) in enumerate([
    ('neg_consequences_employer', 'Neg. Konsequenzen bei MH-Gespräch mit AG'),
    ('neg_consequences_physical', 'Neg. Konsequenzen bei körperl. Gesundheitsgespräch')
]):
    if col in df.columns:
        counts = df[col].value_counts()
        axes_neg[i].bar(range(len(counts)), counts.values, color='steelblue', alpha=0.7)
        axes_neg[i].set_xticks(range(len(counts)))
        axes_neg[i].set_xticklabels(counts.index, rotation=15)
        axes_neg[i].set_title(title, fontsize=10)
        axes_neg[i].set_ylabel('Anzahl')

plt.tight_layout()
plt.savefig(FIGURES_DIR / "dist_neg_consequences_employer.png")
plt.close()

h("Negative Konsequenzen bei Gespräch mit Arbeitgeber", 2)
fig("dist_neg_consequences_employer.png", "Negative Konsequenzen MH vs. körperliche Gesundheit")

# -----------------------------------------------------------------------
# 11. Weitere Verteilungen
# -----------------------------------------------------------------------
plot_cols = [
    ('self_employed', 'Selbstständig?'),
    ('company_size', 'Unternehmensgröße'),
    ('mh_benefits', 'MH-Benefits vom Arbeitgeber?'),
    ('leave_difficulty', 'Wie schwer ist es, MH-Urlaub zu nehmen?'),
    ('neg_consequences_employer', 'Negative Konsequenzen bei AG?'),
    ('comfortable_coworkers', 'MH-Gespräch mit Kollegen ok?'),
    ('comfortable_supervisor', 'MH-Gespräch mit Vorgesetzten ok?'),
    ('current_disorder', 'Aktuelle MH-Störung?'),
    ('past_disorder', 'Frühere MH-Störung?'),
    ('family_history', 'Familiengeschichte MH?'),
    ('sought_treatment', 'Behandlung gesucht?'),
    ('remote_work', 'Remote-Arbeit?'),
]

fig_dist, axes_dist = plt.subplots(4, 3, figsize=(16, 20))
axes_dist = axes_dist.flatten()

for i, (col, title) in enumerate(plot_cols):
    if col in df.columns:
        counts = df[col].value_counts()
        axes_dist[i].barh(range(len(counts)), counts.values, color='steelblue', alpha=0.7)
        axes_dist[i].set_yticks(range(len(counts)))
        axes_dist[i].set_yticklabels(counts.index, fontsize=8)
        axes_dist[i].set_title(title, fontsize=10, fontweight='bold')
        axes_dist[i].invert_yaxis()

plt.tight_layout()
plt.savefig(FIGURES_DIR / "dist_overview.png")
plt.close()

h("Weitere Verteilungen", 2)
fig("dist_overview.png", "Verteilung ausgewählter Variablen")

# -----------------------------------------------------------------------
# Report schreiben
# -----------------------------------------------------------------------
with open(REPORT_PATH, 'w', encoding='utf-8') as f:
    f.write("# EDA Report – OSMI Mental Health in Tech Survey 2016\n\n")
    for line in report_lines:
        f.write(line + "\n")

print(f"Report gespeichert: {REPORT_PATH}")