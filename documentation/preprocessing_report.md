# Preprocessing-Report: Psychische Gesundheit in Tech-Berufen

Erstellt am: 2026-04-17 01:06

## Uebersicht
- Input: 1433 Zeilen, 63 Spalten
- Output: 1428 Zeilen, 63 Spalten

## Verarbeitungsschritte


### 1. Daten geladen
- 1433 Zeilen, 63 Spalten

### 2. Alter bereinigen
- Alter: 5 Zeilen mit unplausiblem Alter entfernt (< 18 oder > 80)
  Entfernte Werte: [3, 15, 17, 99, 323]
- Zeilen vorher: 1433, nachher: 1428

### 3. Gender bereinigen
- Gender: 69 Rohwerte -> 3 Kategorien
  Male: 1055
  Female: 343
  Non-binary: 27

### 4. Country -> Region
- Region: 53 Laender -> 5 Regionen
  North America: 914
  Europe: 409
  Other: 59
  Oceania: 44
  Latin America: 2

### 5. Strukturell fehlende Werte behandeln
- Arbeitgeber-Spalten: 286 Selbststaendige mit 'N/A' gefuellt
- Fruehere-Arbeitgeber-Spalten: 168 Personen ohne fruehere AG mit 'N/A' gefuellt

### 6. Spalten entfernen
- 18 Spalten entfernt: interview_physical_why, interview_mental_why, diagnosed_conditions, believed_conditions, professional_diagnosis_detail, us_state_live, us_state_work, country_work, tech_role, know_resources, reveal_clients, reveal_clients_impact, reveal_coworkers, reveal_coworkers_impact, productivity_affected, pct_work_affected, observations_less_likely, Do you have medical coverage (private insurance or state-provided) which includes treatment of  mental health issues?

### 7. work_position aufloesen
- work_position: 12 Positionen gefunden, 11 als Features behalten (>= 30 Nennungen)
  Back-end Developer: 735
  Front-end Developer: 501
  DevOps/SysAdmin: 282
  Supervisor/Team Lead: 276
  Other: 186
  Support: 168
  One-person shop: 161
  Designer: 135
  Executive Leadership: 101
  Dev Evangelist/Advocate: 99
  Sales: 31

### 8. observed_bad_response kodieren
- observed_bad_response: ordinal kodiert (0-3)

### 9. Ordinale Kodierung
- leave_difficulty: ordinal kodiert (6 Stufen), 0 neue NaN durch Mapping
- share_friends_family: ordinal kodiert (6 Stufen), 0 neue NaN durch Mapping
- interferes_treated: ordinal kodiert (5 Stufen), 555 neue NaN durch Mapping
- interferes_untreated: ordinal kodiert (5 Stufen), 466 neue NaN durch Mapping
- company_size: ordinal kodiert (6 Stufen), 0 neue NaN durch Mapping
- neg_consequences_employer: Yes/No/Maybe -> 2/0/1
- neg_consequences_physical: Yes/No/Maybe -> 2/0/1
- comfortable_coworkers: Yes/No/Maybe -> 2/0/1
- comfortable_supervisor: Yes/No/Maybe -> 2/0/1
- interview_physical: Yes/No/Maybe -> 2/0/1
- interview_mental: Yes/No/Maybe -> 2/0/1
- current_disorder: Yes/No/Maybe -> 2/0/1
- past_disorder: Yes/No/Maybe -> 2/0/1
- employer_discussed_mh: Yes/No/I don't know -> 2/0/1
- employer_resources: Yes/No/I don't know -> 2/0/1
- anonymity_protected: Yes/No/I don't know -> 2/0/1
- employer_takes_mh_serious: Yes/No/I don't know -> 2/0/1
- family_history: Yes/No/I don't know -> 2/0/1
- mh_benefits: ordinal kodiert (No/N-A=0, Don't know=1, Yes=2)
- know_options: ordinal kodiert (0-2)
- mh_hurts_career: ordinal kodiert (0-4)
- coworkers_view_neg: ordinal kodiert (0-4)
- observed_neg_consequences: Yes/No -> 1/0
- professionally_diagnosed: Yes/No -> 1/0

### 10. Fruehere-Arbeitgeber Kodierung
- prev_mh_benefits: ordinal kodiert (0-3)
- prev_aware_options: ordinal kodiert (0-3)
- prev_discussed_mh: ordinal kodiert (0-3)
- prev_resources: ordinal kodiert (0-3)
- prev_anonymity: ordinal kodiert (0-3)
- prev_neg_consequences: ordinal kodiert (0-3)
- prev_neg_physical: ordinal kodiert (0-3)
- prev_comfortable_coworkers: ordinal kodiert (0-2)
- prev_comfortable_supervisor: ordinal kodiert (0-3)
- prev_mh_serious: ordinal kodiert (0-3)
- prev_observed_neg: ordinal kodiert (0-2)

### 11. One-Hot-Encoding
- One-Hot-Encoding: 3 Spalten -> 11 Spalten
  gender
  remote_work
  region

### 12. Verbleibende NaN behandeln
- company_size: 286 NaN mit Median (4.0) gefuellt
- mh_benefits: 286 NaN mit Median (1.0) gefuellt
- know_options: 418 NaN mit Median (1.0) gefuellt
- employer_discussed_mh: 286 NaN mit Median (0.0) gefuellt
- employer_resources: 286 NaN mit Median (1.0) gefuellt
- anonymity_protected: 286 NaN mit Median (1.0) gefuellt
- leave_difficulty: 286 NaN mit Median (3.0) gefuellt
- neg_consequences_employer: 286 NaN mit Median (1.0) gefuellt
- neg_consequences_physical: 286 NaN mit Median (0.0) gefuellt
- comfortable_coworkers: 286 NaN mit Median (1.0) gefuellt
- comfortable_supervisor: 286 NaN mit Median (1.0) gefuellt
- employer_takes_mh_serious: 286 NaN mit Median (1.0) gefuellt
- observed_neg_consequences: 286 NaN mit Median (0.0) gefuellt
- prev_mh_benefits: 168 NaN mit Median (1.0) gefuellt
- prev_aware_options: 168 NaN mit Median (1.0) gefuellt
- prev_discussed_mh: 168 NaN mit Median (0.0) gefuellt
- prev_resources: 168 NaN mit Median (0.0) gefuellt
- prev_anonymity: 168 NaN mit Median (1.0) gefuellt
- prev_neg_consequences: 168 NaN mit Median (2.0) gefuellt
- prev_neg_physical: 168 NaN mit Median (2.0) gefuellt
- prev_comfortable_coworkers: 168 NaN mit Median (1.0) gefuellt
- prev_comfortable_supervisor: 168 NaN mit Median (2.0) gefuellt
- prev_mh_serious: 168 NaN mit Median (1.0) gefuellt
- prev_observed_neg: 168 NaN mit Median (0.0) gefuellt
- observed_bad_response: 88 NaN mit Median (1.0) gefuellt
- interferes_treated: 555 NaN mit Median (3.0) gefuellt
- interferes_untreated: 466 NaN mit Median (1.0) gefuellt
- NaN gesamt: 7093 -> 286
