FIELDS = {
    "categorical": {
        "gender": ['Male', 'Female'],
        "region": ['Northeast', 'Northwest', 'Southeast', 'Southwest'],
        "marital_status": ['Unmarried', 'Married'],
        "bmi_category": ['Overweight', 'Underweight', 'Normal', 'Obesity'],
        "smoking_status": ['Regular', 'No Smoking', 'Occasional'],
        "employment_status": ['Self-Employed', 'Freelancer', 'Salaried'],
        "income_level": ['> 40L', '<10L', '10L - 25L', '25L - 40L'],
        "medical_history": ['Diabetes', 'Heart disease', 'High blood pressure', 'Thyroid'],
        "insurance_plan": ['Silver', 'Bronze', 'Gold']
    },
    "numerical": {
        "age": {"min": 18, "max": 100, "step": 1},
        "income_lakhs": {"min": 0, "max": 200, "step": 1},
        "number_of_dependants": {"min": 0, "max": 20, "step": 1},
        "genetical_risk": {"min": 0, "max": 5, "step": 1}
    }
}

FIELD_ORDER = [
    "age",            "number_of_dependants",
    "income_lakhs",   "income_level",
    "genetical_risk", "gender",
    "marital_status", "employment_status",
    "bmi_category",   "smoking_status",
    "region",         "insurance_plan",
]
