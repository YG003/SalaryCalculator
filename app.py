from flask import Flask, render_template, request, jsonify

# Initialize the Flask app
app = Flask(__name__)

# Route to serve the main form
@app.route('/')
def index():
    # Serve the index1.html file from the 'templates/' directory
    return render_template('index1.html')

# Route to handle salary calculations
@app.route('/calculate', methods=['POST'])
def calculate_salary():
    # Get JSON data from the request
    data = request.json

    # Extract data with default values for safety
    hourly_rate = float(data.get('hourly_rate', 0))
    hours_per_week = float(data.get('hours_per_week', 0))
    overtime_hours = float(data.get('overtime_hours', 0))
    overtime_rate = float(data.get('overtime_rate', 1))
    tax_code = data.get('tax_code', '1257L')
    pension_percent = float(data.get('pension_percent', 0))
    national_insurance = float(data.get('national_insurance', 0))
    student_loan_plan = data.get('student_loan_plan', 'Plan 1')

    # Calculate gross salary
    basic_salary = hourly_rate * hours_per_week * 52  # 4 weeks in a month
    overtime_salary = overtime_hours * hourly_rate * overtime_rate * 52
    gross_salary = basic_salary + overtime_salary

    # Calculate deductions
    tax_deduction = calculate_tax(gross_salary, tax_code)
    ni_deduction = calculate_nic(gross_salary)
    pension_deduction = (pension_percent / 100) * gross_salary
    student_loan_deduction = calculate_student_loan(gross_salary, student_loan_plan)

    # Calculate net salary
    net_salary = gross_salary - (tax_deduction + ni_deduction + pension_deduction + student_loan_deduction)

    # Return the results as JSON
    return jsonify({
        'gross_salary': gross_salary,
        'tax_deduction': tax_deduction,
        'ni_deduction': ni_deduction,
        'pension_deduction': pension_deduction,
        'student_loan_deduction': student_loan_deduction,
        'net_salary': net_salary
    })

# Helper function to calculate tax
def calculate_tax(salary, tax_code):
    """Calculate tax based on salary and tax code."""
    tax_free_allowance = 12570 if tax_code == "1257L" else 0
    taxable_salary = max(0, salary - tax_free_allowance)

    # Basic tax bands
    basic_rate = 0.2 * min(taxable_salary, 50270)
    higher_rate = 0.4 * max(0, taxable_salary - 50270)
    highest_rate = 0.45 * max(0,taxable_salary - 50270)

    return basic_rate + higher_rate + highest_rate

# Helper function to calculate National Insurance contributions
def calculate_nic(salary):
    """Calculate National Insurance contributions."""
    primary_threshold = 12570  # Threshold for NI
    upper_limit = 50270  # Upper limit for 12% rate
    if salary <= primary_threshold:
        return 0
    elif salary <= upper_limit:
        return (salary - primary_threshold) * 0.12
    else:
        return (upper_limit - primary_threshold) * 0.12 + (salary - upper_limit) * 0.02

# Helper function to calculate student loan repayment
def calculate_student_loan(salary, plan):
    """Calculate student loan repayment based on the plan."""
    thresholds = {
        "Plan 1": 22000,
        "Plan 2": 27295,
        "Plan 4": 25375,
        "Postgraduate": 21000
    }
    rates = {
        "Plan 1": 0.09,
        "Plan 2": 0.09,
        "Plan 4": 0.09,
        "Postgraduate": 0.06
    }

    threshold = thresholds.get(plan, 0)
    rate = rates.get(plan, 0)

    return max(0, (salary - threshold) * rate)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
