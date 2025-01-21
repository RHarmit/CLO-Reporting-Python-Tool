import pandas as pd
import numpy as np
from fpdf import FPDF
import matplotlib.pyplot as plt

# Sample Data
def load_data():
    data = {
        'Loan_ID': [1, 2, 3, 4, 5],
        'Sector': ['Technology', 'Healthcare', 'Energy', 'Finance', 'Technology'],
        'Principal': [100000, 200000, 150000, 120000, 130000],
        'Credit_Rating': ['A', 'B', 'BB', 'A', 'BBB']
    }
    return pd.DataFrame(data)

# Compliance Testing
def compliance_testing(df):
    SECTOR_LIMITS = {
        'Technology': 0.4,
        'Healthcare': 0.3,
        'Energy': 0.2,
        'Finance': 0.25
    }

    total_principal = df['Principal'].sum()
    sector_allocation = df.groupby('Sector')['Principal'].sum() / total_principal

    # Convert SECTOR_LIMITS to a Series with matching index
    sector_limits_series = pd.Series(SECTOR_LIMITS)

    # Align sector_allocation with sector_limits_series
    sector_allocation = sector_allocation.reindex(sector_limits_series.index, fill_value=0)

    # Compare to determine compliance
    sector_compliance = sector_allocation <= sector_limits_series

    return df, sector_compliance

# Generate Cashflows
def generate_cashflows(df):
    df['Interest_Rate'] = np.random.uniform(0.03, 0.07, size=len(df))
    df['Cashflow'] = df['Principal'] * df['Interest_Rate']
    return df

# Report Generation
def generate_report(df, sector_compliance):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Collateral Portfolio Report", ln=True, align='C')

    pdf.cell(200, 10, txt="Loan Data:", ln=True, align='L')
    for _, row in df.iterrows():
        pdf.cell(200, 10, txt=f"Loan ID: {row['Loan_ID']}, Sector: {row['Sector']}, Principal: {row['Principal']}, Cashflow: {row['Cashflow']:.2f}", ln=True, align='L')

    pdf.cell(200, 10, txt="Sector Compliance:", ln=True, align='L')
    for sector, compliant in sector_compliance.items():
        status = "Compliant" if compliant else "Non-Compliant"
        pdf.cell(200, 10, txt=f"{sector}: {status}", ln=True, align='L')

    pdf.output("Collateral_Portfolio_Report.pdf")

# Visualize Data
def visualize_data(df):
    sector_totals = df.groupby('Sector')['Principal'].sum()
    sector_totals.plot(kind='bar', title="Principal Allocation by Sector")
    plt.xlabel("Sector")
    plt.ylabel("Total Principal")
    plt.tight_layout()
    plt.savefig("Sector_Allocation.png")
    plt.show()

# Main Function
def main():
    df = load_data()
    df, sector_compliance = compliance_testing(df)
    df = generate_cashflows(df)
    generate_report(df, sector_compliance)
    visualize_data(df)

if __name__ == "__main__":
    main()