import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(".")
INPUT_FILE = "data/raw/mental-health-in-tech-2016_20161114.csv"
OUTPUT_FILE = "data/processed/mental_heath_cleaned.csv"
REPORT_FILE = "documentation/preprocessing_report.md"

# Spalten-Namen, aus EDA-Script
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
    "Do you have medical coverage (private insurance or state-provided) which includes treatment of  mental health issues?": "medical_coverage",
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

# Gender normalisieren
GENDER_MAP = {
    # Male
    "male": "Male", "m": "Male", "male ": "Male", "male.": "Male",
    "cis male": "Male", "cis man": "Male", "cisdude": "Male",
    "male (cis)": "Male", "man": "Male", "dude": "Male",
    "sex is male": "Male", "malr": "Male", "mail": "Male",
    "m|": "Male", "male (trans, ftm)": "Male",
    "i'm a man why didn't you make this a drop down question. you should of asked sex? and i would of answered yes please. seriously how much text can this take?": "Male",
    "male 9:1 female, roughly": "Male",
    # Female
    "female": "Female", "f": "Female", "female ": "Female",
    "cis female": "Female", "cis-woman": "Female", "woman": "Female",
    "cisgender female": "Female", "fem": "Female", "fm": "Female",
    "female/woman": "Female", "female assigned at birth": "Female",
    "i identify as female.": "Female",
    "female (props for making this a freeform field, though)": "Female",
    "female-bodied; no feelings about gender": "Female",
    "transitioned, m2f": "Female", "mtf": "Female",
    "transgender woman": "Female",
    "female or multi-gender femme": "Female",
    # Non-binary
    "non-binary": "Non-binary", "nonbinary": "Non-binary",
    "genderqueer": "Non-binary", "genderqueer woman": "Non-binary",
    "genderfluid": "Non-binary", "genderfluid (born female)": "Non-binary",
    "genderflux demi-girl": "Non-binary", "agender": "Non-binary",
    "androgynous": "Non-binary", "bigender": "Non-binary",
    "enby": "Non-binary", "fluid": "Non-binary", "queer": "Non-binary",
    "nb masculine": "Non-binary", "other": "Non-binary",
    "other/transfeminine": "Non-binary", "male/genderqueer": "Non-binary",
    "afab": "Non-binary", "human": "Non-binary",
    "none of your business": "Non-binary", "unicorn": "Non-binary",
}

# Spalten fuer Angestellte
EMPLOYER_COLUMNS = [
    "company_size", "tech_company", "mh_benefits", "know_options",
    "employer_discussed_mh", "employer_resources", "anonymity_protected",
    "leave_difficulty", "neg_consequences_employer", "neg_consequences_physical",
    "comfortable_coworkers", "comfortable_supervisor",
    "employer_takes_mh_serious", "observed_neg_consequences",
]

# Fruehere Arbeitgeber, falls vorhanden
PREV_EMPLOYER_COLUMNS = [
    "prev_mh_benefits", "prev_aware_options", "prev_discussed_mh",
    "prev_resources", "prev_anonymity", "prev_neg_consequences",
    "prev_neg_physical", "prev_comfortable_coworkers",
    "prev_comfortable_supervisor", "prev_mh_serious", "prev_observed_neg",
]

# Spalten loeschen
DROP_COLUMNS = [
    "interview_physical_why", "interview_mental_why",
    "diagnosed_conditions", "believed_conditions",
    "professional_diagnosis_detail",
    "us_state_live", "us_state_work",
    "country_work",  # fast identisch mit country_live
    "tech_role",  # 81.6% fehlend
    "medical_coverage",  # 80% fehlend (nur Selbststaendige)
    "know_resources",  # 80% fehlend
    "reveal_clients", "reveal_clients_impact",  # 80-90% fehlend
    "reveal_coworkers", "reveal_coworkers_impact",  # 80% fehlend
    "productivity_affected", "pct_work_affected",  # 80-86% fehlend
    "observations_less_likely",  # 54% fehlend
    "Do you have medical coverage (private insurance or state-provided) which includes treatment of \xa0mental health issues?",
]

# Mappings fuer Ranking-Spalten
ORDINAL_MAPS = {
    "leave_difficulty": {
        "Very difficult": 1, "Somewhat difficult": 2,
        "Neither easy nor difficult": 3, "I don't know": 3,
        "Somewhat easy": 4, "Very easy": 5,
    },
    "share_friends_family": {
        "Not open at all": 1, "Somewhat not open": 2,
        "Neutral": 3, "Not applicable to me (I do not have a mental illness)": 3,
        "Somewhat open": 4, "Very open": 5,
    },
    "interferes_treated": {
        "Often": 1, "Sometimes": 2, "Rarely": 3, "Never": 4,
        "Not applicable to me": np.nan,
    },
    "interferes_untreated": {
        "Often": 1, "Sometimes": 2, "Rarely": 3, "Never": 4,
        "Not applicable to me": np.nan,
    },
    "company_size": {
        "1-5": 1, "6-25": 2, "26-100": 3,
        "100-500": 4, "500-1000": 5, "More than 1000": 6,
    },
}

# Yes/No/Maybe
YES_NO_MAYBE_MAP = {"Yes": 2, "Maybe": 1, "No": 0}
YES_NO_MAP = {"Yes": 1, "No": 0}
YES_NO_DONTKNOW_MAP = {"Yes": 2, "I don't know": 1, "No": 0}

# Spalten mit Yes/No/Maybe
YES_NO_MAYBE_COLUMNS = [
    "neg_consequences_employer", "neg_consequences_physical",
    "comfortable_coworkers", "comfortable_supervisor",
    "interview_physical", "interview_mental",
    "current_disorder", "past_disorder",
]

# Spalten mit Yes/No/I don't know
YES_NO_DONTKNOW_COLUMNS = [
    "employer_discussed_mh", "employer_resources", "anonymity_protected",
    "employer_takes_mh_serious", "family_history",
]

# Country, Aggregation 
REGION_MAP = {
    "United States of America": "North America",
    "Canada": "North America",
    "Mexico": "Latin America",
    "United Kingdom": "Europe",
    "Germany": "Europe",
    "Netherlands": "Europe",
    "France": "Europe",
    "Sweden": "Europe",
    "Ireland": "Europe",
    "Switzerland": "Europe",
    "Denmark": "Europe",
    "Finland": "Europe",
    "Belgium": "Europe",
    "Italy": "Europe",
    "Poland": "Europe",
    "Spain": "Europe",
    "Austria": "Europe",
    "Romania": "Europe",
    "Czech Republic": "Europe",
    "Norway": "Europe",
    "Bulgaria": "Europe",
    "Lithuania": "Europe",
    "Estonia": "Europe",
    "Bosnia and Herzegovina": "Europe",
    "Slovakia": "Europe",
    "Greece": "Europe",
    "Hungary": "Europe",
    "Serbia": "Europe",
    "Australia": "Oceania",
    "New Zealand": "Oceania",
}

def load_and_rename(filepath):
    """Laedt CSV und benennt Spalten um."""
    df = pd.read_csv(filepath)
    rename_map = {k: v for k, v in COLUMN_ALIASES.items() if k in df.columns}
    df.rename(columns=rename_map, inplace=True)
    if "Why or why not?.1" in df.columns:
        df.rename(columns={"Why or why not?.1": "interview_mental_why"}, inplace=True)
    return df


def clean_age(df, log):
    """Bereinigt Alter: Ausreisser entfernen oder korrigieren."""
    before = len(df)
    df["age"] = pd.to_numeric(df["age"], errors="coerce")

    # Offensichtliche Fehler: Alter < 18 oder > 80 entfernen
    invalid = df[(df["age"] < 18) | (df["age"] > 80)]
    log.append(f"- Alter: {len(invalid)} Zeilen mit unplausiblem Alter entfernt (< 18 oder > 80)")
    log.append(f"  Entfernte Werte: {sorted(invalid['age'].dropna().unique().tolist())}")
    df = df[(df["age"] >= 18) & (df["age"] <= 80)].copy()

    after = len(df)
    log.append(f"- Zeilen vorher: {before}, nachher: {after}")
    return df


def clean_gender(df, log):
    """Bereinigt Gender-Spalte auf Male/Female/Non-binary."""
    def map_gender(val):
        if pd.isna(val):
            return np.nan
        key = str(val).strip().lower()
        return GENDER_MAP.get(key, "Non-binary")

    before_unique = df["gender"].nunique()
    df["gender"] = df["gender"].apply(map_gender)
    after_unique = df["gender"].nunique()

    counts = df["gender"].value_counts()
    log.append(f"- Gender: {before_unique} Rohwerte -> {after_unique} Kategorien")
    for cat, n in counts.items():
        log.append(f"  {cat}: {n}")

    return df


def clean_country(df, log):
    """Erzeugt Region-Spalte aus Country und entfernt Country."""
    def map_region(country):
        if pd.isna(country):
            return "Other"
        return REGION_MAP.get(country, "Other")

    df["region"] = df["country_live"].apply(map_region)
    counts = df["region"].value_counts()
    log.append(f"- Region: {df['country_live'].nunique()} Laender -> {df['region'].nunique()} Regionen")
    for reg, n in counts.items():
        log.append(f"  {reg}: {n}")

    df.drop(columns=["country_live"], inplace=True)
    return df


def handle_employer_missing(df, log):
    """Fuellt fehlende Arbeitgeber-Spalten bei Selbststaendigen mit 'N/A'."""
    self_emp_mask = df["self_employed"] == 1
    n_self = self_emp_mask.sum()

    for col in EMPLOYER_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype(object)
            df.loc[self_emp_mask, col] = np.nan

    log.append(f"- Arbeitgeber-Spalten: {n_self} Selbststaendige mit 'N/A' gefuellt")
    return df


def handle_prev_employer_missing(df, log):
    """Fuellt fehlende Spalten bei Personen ohne fruehere Arbeitgeber."""
    no_prev_mask = df["has_previous_employers"] == 0
    n_no_prev = no_prev_mask.sum()

    for col in PREV_EMPLOYER_COLUMNS:
        if col in df.columns:
            df.loc[no_prev_mask, col] = np.nan

    log.append(f"- Fruehere-Arbeitgeber-Spalten: {n_no_prev} Personen ohne fruehere AG mit 'N/A' gefuellt")
    return df


def drop_columns(df, log):
    """Entfernt Spalten mit zu vielen fehlenden Werten oder Freitext."""
    cols_to_drop = [c for c in DROP_COLUMNS if c in df.columns]
    df.drop(columns=cols_to_drop, inplace=True)
    log.append(f"- {len(cols_to_drop)} Spalten entfernt: {', '.join(cols_to_drop)}")
    return df


def extract_work_position_features(df, log):
    """Extrahiert Mehrfachnennungen bei work_position in binaere Features."""
    positions = set()
    for val in df["work_position"].dropna():
        for pos in str(val).split("|"):
            positions.add(pos.strip())

    # Nur die haeufigsten behalten (mind. 30 Nennungen)
    pos_counts = {}
    for pos in positions:
        count = df["work_position"].dropna().apply(lambda x: pos in str(x)).sum()
        pos_counts[pos] = count

    kept_positions = {p: c for p, c in pos_counts.items() if c >= 30}

    for pos in sorted(kept_positions.keys()):
        col_name = f"pos_{pos.lower().replace(' ', '_').replace('/', '_').replace('-', '_')}"
        df[col_name] = df["work_position"].apply(
            lambda x: 1 if pd.notna(x) and pos in str(x) else 0
        )

    log.append(f"- work_position: {len(positions)} Positionen gefunden, {len(kept_positions)} als Features behalten (>= 30 Nennungen)")
    for pos, count in sorted(kept_positions.items(), key=lambda x: x[1], reverse=True):
        log.append(f"  {pos}: {count}")

    df.drop(columns=["work_position"], inplace=True)
    return df


def extract_condition_feature(df, log):
    """Erzeugt Feature fuer Anzahl diagnostizierter Bedingungen (aus observed_bad_response)."""
    # observed_bad_response hat 4 Kategorien -> ordinal mappen
    obs_map = {
        "No": 0,
        "Maybe/Not sure": 1,
        "Yes, I observed": 2,
        "Yes, I experienced": 3,
    }
    if "observed_bad_response" in df.columns:
        df["observed_bad_response"] = df["observed_bad_response"].map(obs_map)
        log.append(f"- observed_bad_response: ordinal kodiert (0-3)")
    return df


def encode_ordinal(df, log):
    """Kodiert ordinale Spalten numerisch."""
    for col, mapping in ORDINAL_MAPS.items():
        if col in df.columns:
            before_na = df[col].isna().sum()
            df[col] = df[col].map(mapping)
            after_na = df[col].isna().sum()
            new_na = after_na - before_na
            log.append(f"- {col}: ordinal kodiert ({len(mapping)} Stufen), {new_na} neue NaN durch Mapping")

    return df


def encode_yes_no(df, log):
    """Kodiert Yes/No/Maybe und aehnliche Spalten."""
    for col in YES_NO_MAYBE_COLUMNS:
        if col in df.columns:
            df[col] = df[col].map(YES_NO_MAYBE_MAP)
            log.append(f"- {col}: Yes/No/Maybe -> 2/0/1")

    for col in YES_NO_DONTKNOW_COLUMNS:
        if col in df.columns:
            df[col] = df[col].map(YES_NO_DONTKNOW_MAP)
            log.append(f"- {col}: Yes/No/I don't know -> 2/0/1")

    return df


def encode_mh_benefits(df, log):
    """Kodiert mh_benefits ordinal."""
    mapping = {
        "No": 0, "Not eligible for coverage / N/A": 0,
        "I don't know": 1, "Yes": 2, "N/A": np.nan,
    }
    if "mh_benefits" in df.columns:
        df["mh_benefits"] = df["mh_benefits"].map(mapping)
        log.append(f"- mh_benefits: ordinal kodiert (No/N-A=0, Don't know=1, Yes=2)")
    return df


def encode_know_options(df, log):
    """Kodiert know_options ordinal."""
    mapping = {"No": 0, "I am not sure": 1, "Yes": 2}
    if "know_options" in df.columns:
        df["know_options"] = df["know_options"].map(mapping)
        log.append(f"- know_options: ordinal kodiert (0-2)")
    return df


def encode_mh_hurts_career(df, log):
    """Kodiert mh_hurts_career ordinal."""
    mapping = {
        "No, it has not": 0, "No, I don't think it would": 1,
        "Maybe": 2, "Yes, I think it would": 3, "Yes, it has": 4,
    }
    if "mh_hurts_career" in df.columns:
        df["mh_hurts_career"] = df["mh_hurts_career"].map(mapping)
        log.append(f"- mh_hurts_career: ordinal kodiert (0-4)")
    return df


def encode_coworkers_view_neg(df, log):
    """Kodiert coworkers_view_neg ordinal."""
    mapping = {
        "No, they do not": 0, "No, I don't think they would": 1,
        "Maybe": 2, "Yes, I think they would": 3, "Yes, they do": 4,
    }
    if "coworkers_view_neg" in df.columns:
        df["coworkers_view_neg"] = df["coworkers_view_neg"].map(mapping)
        log.append(f"- coworkers_view_neg: ordinal kodiert (0-4)")
    return df


def encode_observed_neg_consequences(df, log):
    """Kodiert observed_neg_consequences."""
    if "observed_neg_consequences" in df.columns:
        df["observed_neg_consequences"] = df["observed_neg_consequences"].map(YES_NO_MAP)
        log.append(f"- observed_neg_consequences: Yes/No -> 1/0")
    return df

def encode_professionally_diagnosed(df, log):
    """Kodiert professionally_diagnosed."""
    if "professionally_diagnosed" in df.columns:
        df["professionally_diagnosed"] = df["professionally_diagnosed"].map({"Yes": 1, "No": 0})
        log.append(f"- professionally_diagnosed: Yes/No -> 1/0")
    return df

def encode_prev_employer_columns(df, log):
    """Kodiert prev_employer Spalten."""
    # prev_mh_benefits
    mapping = {
        "No, none did": 0, "I don't know": 1,
        "Some did": 2, "Yes, they all did": 3, "N/A": np.nan,
    }
    if "prev_mh_benefits" in df.columns:
        df["prev_mh_benefits"] = df["prev_mh_benefits"].map(mapping)
        log.append(f"- prev_mh_benefits: ordinal kodiert (0-3)")

    # prev_aware_options
    mapping = {
        "N/A (not currently aware)": 0, "No, I only became aware later": 1,
        "I was aware of some": 2, "Yes, I was aware of all of them": 3, "N/A": np.nan,
    }
    if "prev_aware_options" in df.columns:
        df["prev_aware_options"] = df["prev_aware_options"].map(mapping)
        log.append(f"- prev_aware_options: ordinal kodiert (0-3)")

    # prev_discussed_mh
    mapping = {
        "None did": 0, "I don't know": 1,
        "Some did": 2, "Yes, they all did": 3, "N/A": np.nan,
    }
    for col in ["prev_discussed_mh", "prev_resources"]:
        if col in df.columns:
            df[col] = df[col].map(mapping)
            log.append(f"- {col}: ordinal kodiert (0-3)")

    # prev_anonymity
    mapping = {
        "No": 0, "I don't know": 1, "Sometimes": 2,
        "Yes, always": 3, "N/A": np.nan,
    }
    if "prev_anonymity" in df.columns:
        df["prev_anonymity"] = df["prev_anonymity"].map(mapping)
        log.append(f"- prev_anonymity: ordinal kodiert (0-3)")

    # prev_neg_consequences / prev_neg_physical
    mapping = {
        "None of them": 0, "I don't know": 1,
        "Some of them": 2, "Yes, all of them": 3, "N/A": np.nan,
    }
    for col in ["prev_neg_consequences", "prev_neg_physical"]:
        if col in df.columns:
            df[col] = df[col].map(mapping)
            log.append(f"- {col}: ordinal kodiert (0-3)")

    # prev_comfortable_coworkers
    mapping = {
        "No, at none of my previous employers": 0,
        "Some of my previous employers": 1,
        "Yes, at all of my previous employers": 2, "N/A": np.nan,
    }
    if "prev_comfortable_coworkers" in df.columns:
        df["prev_comfortable_coworkers"] = df["prev_comfortable_coworkers"].map(mapping)
        log.append(f"- prev_comfortable_coworkers: ordinal kodiert (0-2)")

    # prev_comfortable_supervisor
    mapping = {
        "No, at none of my previous employers": 0,
        "I don't know": 1,
        "Some of my previous employers": 2,
        "Yes, at all of my previous employers": 3, "N/A": np.nan,
    }
    if "prev_comfortable_supervisor" in df.columns:
        df["prev_comfortable_supervisor"] = df["prev_comfortable_supervisor"].map(mapping)
        log.append(f"- prev_comfortable_supervisor: ordinal kodiert (0-3)")

    # prev_mh_serious
    mapping = {
        "None did": 0, "I don't know": 1,
        "Some did": 2, "Yes, they all did": 3, "N/A": np.nan,
    }
    if "prev_mh_serious" in df.columns:
        df["prev_mh_serious"] = df["prev_mh_serious"].map(mapping)
        log.append(f"- prev_mh_serious: ordinal kodiert (0-3)")

    # prev_observed_neg
    mapping = {
        "None of them": 0, "Some of them": 1,
        "Yes, all of them": 2, "N/A": np.nan,
    }
    if "prev_observed_neg" in df.columns:
        df["prev_observed_neg"] = df["prev_observed_neg"].map(mapping)
        log.append(f"- prev_observed_neg: ordinal kodiert (0-2)")

    return df


def encode_remaining_categorical(df, log):
    """One-Hot-Encoding fuer verbleibende kategorische Spalten."""
    cat_cols = ["gender", "remote_work", "region"]
    cat_cols = [c for c in cat_cols if c in df.columns]

    before_cols = len(df.columns)
    df = pd.get_dummies(df, columns=cat_cols, drop_first=False, dtype=int)
    after_cols = len(df.columns)

    log.append(f"- One-Hot-Encoding: {len(cat_cols)} Spalten -> {after_cols - before_cols + len(cat_cols)} Spalten")
    for col in cat_cols:
        log.append(f"  {col}")

    return df


def handle_remaining_na(df, log):
    """Behandelt verbleibende NaN-Werte."""
    na_before = df.isna().sum().sum()

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isna().any():
            median_val = df[col].median()
            n_filled = df[col].isna().sum()
            df[col] = df[col].fillna(median_val)
            log.append(f"- {col}: {n_filled} NaN mit Median ({median_val:.1f}) gefuellt")

    na_after = df.isna().sum().sum()
    log.append(f"- NaN gesamt: {na_before} -> {na_after}")

    return df

def write_report(log, df_before_shape, df_after_shape, output_path):
    """Schreibt Preprocessing-Report als Markdown."""
    md = []
    md.append("# Preprocessing-Report: Psychische Gesundheit in Tech-Berufen")
    md.append(f"\nErstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    md.append("")
    md.append("## Uebersicht")
    md.append(f"- Input: {df_before_shape[0]} Zeilen, {df_before_shape[1]} Spalten")
    md.append(f"- Output: {df_after_shape[0]} Zeilen, {df_after_shape[1]} Spalten")
    md.append("")
    md.append("## Verarbeitungsschritte")
    md.append("")
    for line in log:
        md.append(line)
    md.append("")

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(md))
    print(f"Report gespeichert: {output_path}")

def main():
    log = []
    full_path = PROJECT_ROOT / INPUT_FILE

    # 1. Laden
    df = load_and_rename(full_path)
    df_before_shape = df.shape
    print(f"Geladen: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")
    log.append(f"\n### 1. Daten geladen")
    log.append(f"- {df.shape[0]} Zeilen, {df.shape[1]} Spalten")

    # 2. Alter bereinigen
    log.append(f"\n### 2. Alter bereinigen")
    df = clean_age(df, log)

    # 3. Gender bereinigen
    log.append(f"\n### 3. Gender bereinigen")
    df = clean_gender(df, log)

    # 4. Country -> Region
    log.append(f"\n### 4. Country -> Region")
    df = clean_country(df, log)

    # 5. Strukturell fehlende Werte
    log.append(f"\n### 5. Strukturell fehlende Werte behandeln")
    df = handle_employer_missing(df, log)
    df = handle_prev_employer_missing(df, log)

    # 6. Spalten entfernen
    log.append(f"\n### 6. Spalten entfernen")
    df = drop_columns(df, log)

    # 7. work_position -> binaere Features
    log.append(f"\n### 7. work_position aufloesen")
    df = extract_work_position_features(df, log)

    # 8. observed_bad_response
    log.append(f"\n### 8. observed_bad_response kodieren")
    df = extract_condition_feature(df, log)

    # 9. Ordinale Kodierung
    log.append(f"\n### 9. Ordinale Kodierung")
    df = encode_ordinal(df, log)
    df = encode_yes_no(df, log)
    df = encode_mh_benefits(df, log)
    df = encode_know_options(df, log)
    df = encode_mh_hurts_career(df, log)
    df = encode_coworkers_view_neg(df, log)
    df = encode_observed_neg_consequences(df, log)
    df = encode_professionally_diagnosed(df, log)

    # 10. Prev-Employer Kodierung
    log.append(f"\n### 10. Fruehere-Arbeitgeber Kodierung")
    df = encode_prev_employer_columns(df, log)

    # 11. One-Hot-Encoding
    log.append(f"\n### 11. One-Hot-Encoding")
    df = encode_remaining_categorical(df, log)

    # 12. Verbleibende NaN
    log.append(f"\n### 12. Verbleibende NaN behandeln")
    df = handle_remaining_na(df, log)

    # Speichern
    output_path = PROJECT_ROOT / OUTPUT_FILE
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"\nBereinigte Daten gespeichert: {output_path}")
    print(f"Shape: {df.shape[0]} Zeilen, {df.shape[1]} Spalten")

    # Report
    report_path = PROJECT_ROOT / REPORT_FILE
    write_report(log, df_before_shape, df.shape, report_path)
    print(f"  Input:  {df_before_shape[0]} x {df_before_shape[1]}")
    print(f"  Output: {df.shape[0]} x {df.shape[1]}")
    print(f"  NaN: {df.isna().sum().sum()}")
    print(f"  Datentypen: {df.dtypes.value_counts().to_dict()}")


if __name__ == "__main__":
    main()
