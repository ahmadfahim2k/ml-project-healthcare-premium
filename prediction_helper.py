import pandas as pd
from joblib import load
import os

MODEL_PATH = {
        'model_rest': 'artifacts/model_rest.joblib',
        'model_young': 'artifacts/model_young.joblib',
        'scaler_rest': 'artifacts/scaler_rest.joblib',
        'scaler_young': 'artifacts/scaler_young.joblib',
    }

# Load models and scalers
model_rest = load(MODEL_PATH["model_rest"])
model_young = load(MODEL_PATH["model_young"])
scaler_rest = load(MODEL_PATH["scaler_rest"])
scaler_young = load(MODEL_PATH["scaler_young"])

expected_columns = [ 'age', 'number_of_dependants', 'income_lakhs', 'insurance_plan', 'genetical_risk', 'normalized_risk_score', 'gender_Male', 'region_Northwest', 'region_Southeast', 'region_Southwest', 'marital_status_Unmarried', 'bmi_category_Obesity', 'bmi_category_Overweight', 'bmi_category_Underweight', 'smoking_status_Occasional', 'smoking_status_Regular', 'employment_status_Salaried', 'employment_status_Self-Employed']


# --------------------------
# Dictionaries
# --------------------------
risk_scores_dictionary = {
    'diabetes': 6,
    'heart disease': 8,
    'high blood pressure': 6,
    'thyroid': 5,
    'no disease': 0,
    'none': 0
}

insurance_plan_dictionary = {
    'Bronze': 1,
    'Silver': 2,
    'Gold': 3,
}

income_level_dictionary = {
    '<10L': 1,
    '10L - 25L': 2,
    '25L - 40L': 3,
    '> 40L': 4,
}


def preprocess_input(input_dict, expected_columns):
    """
    Convert raw user input into a model-ready DataFrame with all expected columns.
    """
    # Start with all zeros
    data = {col: 0 for col in expected_columns}

    # --- 1) Fill direct numerical features ---
    numeric_fields = ['age', 'number_of_dependants', 'income_lakhs', 'genetical_risk']
    for field in numeric_fields:
        if field in input_dict:
            data[field] = input_dict[field]

    # --- 2) Handle insurance_plan mapping ---
    if "insurance_plan" in expected_columns and "insurance_plan" in input_dict:
        plan = input_dict["insurance_plan"]
        data["insurance_plan"] = insurance_plan_dictionary.get(plan, 0)

    # --- 3) Handle income_level mapping ---
    if "income_level" in expected_columns and "income_level" in input_dict:
        income_level = input_dict["income_level"]
        data["income_level"] = income_level_dictionary.get(income_level, 0)

    # --- 4) Compute total_risk_score ---
    if "medical_history" in input_dict:
        diseases = input_dict["medical_history"].lower().split("&")
        total_risk_score = sum(
            risk_scores_dictionary.get(d.strip(), 0) for d in diseases
        )
        data["total_risk_score"] = total_risk_score

        # --- 5) Compute normalized_risk_score ---
        min_score = min(risk_scores_dictionary.values())
        max_score = max(risk_scores_dictionary.values())
        if max_score != min_score:
            data["normalized_risk_score"] = (total_risk_score - min_score) / (max_score - min_score)
        else:
            data["normalized_risk_score"] = 0

    # --- 6) One-hot encode categorical values ---
    for col in expected_columns:
        if "_" in col and col not in ("normalized_risk_score", "total_risk_score"):
            feature_name, feature_value = col.rsplit("_", 1)
            if feature_name in input_dict and str(input_dict[feature_name]) == feature_value:
                data[col] = 1

    input_df = pd.DataFrame([data])
    input_df.drop('total_risk_score', axis='columns', inplace=True)
    return input_df

def handle_scaling(age, df):
    age_value = df['age'].iloc[0]  # or .item()
    if (age_value <= 25):
        scaler_object = scaler_young
    else:
        scaler_object = scaler_rest
    
    cols_to_scale = scaler_object['cols_to_scale']
    scaler = scaler_object['scaler']
    
    df['income_level'] = 0

    df[cols_to_scale] = scaler.transform(df[cols_to_scale])
    df.drop('income_level', axis='columns', inplace=True)
    return df

def predict(user_input):
    input_df = preprocess_input(user_input, expected_columns)
    age_value = input_df['age'].iloc[0] 
    input_df = handle_scaling(age_value, input_df)

    if(age_value <= 25):
        prediction = model_young.predict(input_df)
    else:
        prediction = model_rest.predict(input_df)
    return int(prediction)