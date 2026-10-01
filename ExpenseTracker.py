import json
import os
from collections import defaultdict
from datetime import date

import pandas as pd
import streamlit as st


# =========================================================
# CONFIGURATION
# =========================================================

FILE_NAME = "expenses.json"

CATEGORIES = [
    "Food",
    "Travel",
    "Shopping",
    "Bills",
    "Education",
    "Entertainment",
    "Health",
    "Other"
]


# =========================================================
# JSON FILE FUNCTIONS
# =========================================================

def create_json_file():
    """Create the JSON file if it does not exist."""
    if not os.path.exists(FILE_NAME):
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump([], file, indent=4)


def load_expenses():
    """Load expenses from the JSON file."""
    create_json_file()

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_expenses(expenses):
    """Save expenses to the JSON file."""
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            json.dump(expenses, file, indent=4)

        return True

    except OSError:
        return False


# =========================================================
# CRUD FUNCTIONS
# =========================================================

def add_expense(
    name,
    amount,
    category,
    expense_date,
    description
):
    """Create a new expense."""

    expenses = st.session_state.expenses

    new_id = max(
        (
            int(expense.get("id", 0))
            for expense in expenses
        ),
        default=0
    ) + 1

    new_expense = {
        "id": new_id,
        "name": name.strip(),
        "amount": float(amount),
        "category": category,
        "date": str(expense_date),
        "description": description.strip()
    }

    expenses.append(new_expense)

    return save_expenses(expenses)


def update_expense(
    expense_id,
    name,
    amount,
    category,
    expense_date,
    description
):
    """Update an existing expense."""

    for expense in st.session_state.expenses:

        if expense.get("id") == expense_id:

            expense.update({
                "name": name.strip(),
                "amount": float(amount),
                "category": category,
                "date": str(expense_date),
                "description": description.strip()
            })

            return save_expenses(
                st.session_state.expenses
            )

    return False


def delete_expense(expense_id):
    """Delete an expense."""

    st.session_state.expenses = [
        expense
        for expense in st.session_state.expenses
        if expense.get("id") != expense_id
    ]

    return save_expenses(
        st.session_state.expenses
    )


# =========================================================
# VALIDATION
# =========================================================

def validate_expense(
    name,
    amount,
    category,
    expense_date
):
    """Validate expense information."""

    if not name.strip():
        return "Expense name is required."

    if not category:
        return "Category is required."

    if expense_date is None:
        return "Date is required."

    try:
        value = float(amount)

    except (ValueError, TypeError):
        return "Amount must be a valid number."

    if value <= 0:
        return "Amount must be greater than zero."

    return None


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# PROFESSIONAL DESIGN
# =========================================================

st.markdown(
    """
<style>

@import url(
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap'
);


/* =====================================================
   GLOBAL
===================================================== */

html,
body,
[class*="css"] {
    font-family: "Inter", sans-serif;
}


.stApp {

    background:
        linear-gradient(
            135deg,
            #f8fafc 0%,
            #eef2ff 50%,
            #fdf2f8 100%
        );

}


.block-container {

    max-width: 1250px;

    padding-top: 2rem;
    padding-bottom: 3rem;

}


/* =====================================================
   HERO
===================================================== */

.hero {

    background:
        linear-gradient(
            120deg,
            #4f46e5 0%,
            #7c3aed 52%,
            #db2777 100%
        );

    padding: 2.5rem;

    border-radius: 26px;

    margin-bottom: 1.5rem;

    color: white;

    box-shadow:
        0 20px 50px
        rgba(79, 70, 229, 0.25);

}


.hero-title {

    font-size: 2.6rem;

    font-weight: 800;

    letter-spacing: -0.04em;

    line-height: 1.15;

}


.hero-subtitle {

    margin-top: 0.55rem;

    font-size: 1rem;

    opacity: 0.92;

}


/* =====================================================
   SECTION TITLES
===================================================== */

.section-title {

    color: #111827;

    font-size: 1.35rem;

    font-weight: 800;

    margin-top: 1.7rem;

    margin-bottom: 0.85rem;

}


/* =====================================================
   METRIC CARDS
===================================================== */

.metric-card {

    background:
        rgba(255, 255, 255, 0.88);

    border:
        1px solid
        rgba(255, 255, 255, 0.95);

    border-radius: 20px;

    padding: 1.25rem;

    box-shadow:
        0 10px 30px
        rgba(15, 23, 42, 0.07);

}


.metric-label {

    color: #64748b;

    font-size: 0.76rem;

    font-weight: 700;

    text-transform: uppercase;

    letter-spacing: 0.08em;

}


.metric-value {

    color: #0f172a;

    font-size: 1.75rem;

    font-weight: 800;

    margin-top: 0.25rem;

}


/* =====================================================
   FORM
===================================================== */

div[data-testid="stForm"] {

    background:
        rgba(255, 255, 255, 0.88);

    border:
        1px solid #e2e8f0;

    border-radius: 22px;

    padding: 1.35rem;

    box-shadow:
        0 10px 30px
        rgba(15, 23, 42, 0.06);

}


/* =====================================================
   BUTTONS
===================================================== */

.stButton > button,
.stFormSubmitButton > button {

    border-radius: 11px;

    font-weight: 700;

    transition:
        all 0.2s ease;

}


.stButton > button:hover,
.stFormSubmitButton > button:hover {

    transform:
        translateY(-1px);

    box-shadow:
        0 7px 18px
        rgba(79, 70, 229, 0.15);

}


/* =====================================================
   CHART PANELS
===================================================== */

.chart-panel {

    background:
        rgba(255, 255, 255, 0.84);

    border:
        1px solid #e2e8f0;

    border-radius: 20px;

    padding: 1rem 1.2rem 0.7rem;

    box-shadow:
        0 8px 28px
        rgba(15, 23, 42, 0.06);

}


.chart-title {

    color: #111827;

    font-weight: 800;

    font-size: 1rem;

}


/* =====================================================
   FOOTER
===================================================== */

.footer {

    text-align: center;

    color: #64748b;

    font-size: 0.84rem;

    padding-top: 1rem;

}

</style>
""",
    unsafe_allow_html=True
)


# =========================================================
# SESSION STATE
# =========================================================

if "expenses" not in st.session_state:

    st.session_state.expenses = load_expenses()


if "edit_id" not in st.session_state:

    st.session_state.edit_id = None


expenses = st.session_state.expenses


# =========================================================
# CALCULATE DASHBOARD VALUES
# =========================================================

total_amount = sum(
    float(expense.get("amount", 0))
    for expense in expenses
)


expense_count = len(expenses)


average_amount = (
    total_amount / expense_count
    if expense_count > 0
    else 0
)


# =========================================================
# HERO SECTION
# =========================================================

st.markdown(
    '<div class="hero">'
    '<div class="hero-title">💸 Expense Tracker</div>'
    '<div class="hero-subtitle">'
    'Manage your spending, understand your habits, '
    'and stay in control of your money.'
    '</div>'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# DASHBOARD CARDS
# =========================================================

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Total Spending</div>'
        f'<div class="metric-value">'
        f'₹{total_amount:,.2f}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with col2:

    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Total Expenses</div>'
        f'<div class="metric-value">'
        f'{expense_count}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


with col3:

    st.markdown(
        f'<div class="metric-card">'
        f'<div class="metric-label">Average Expense</div>'
        f'<div class="metric-value">'
        f'₹{average_amount:,.2f}'
        f'</div>'
        f'</div>',
        unsafe_allow_html=True
    )


# =========================================================
# ADD EXPENSE
# =========================================================

st.markdown(
    '<div class="section-title">'
    '➕ Add a New Expense'
    '</div>',
    unsafe_allow_html=True
)


with st.form(
    "expense_form",
    clear_on_submit=True
):

    col1, col2 = st.columns(2)


    with col1:

        expense_name = st.text_input(
            "Expense Name *",
            placeholder="e.g. Lunch, Bus ticket, Books"
        )


        amount = st.text_input(
            "Amount *",
            placeholder="e.g. 250"
        )


        category = st.selectbox(
            "Category *",
            CATEGORIES
        )


    with col2:

        expense_date = st.date_input(
            "Date *",
            value=date.today()
        )


        description = st.text_area(
            "Description",
            placeholder="Add a short note...",
            height=122
        )


    submit = st.form_submit_button(
        "💾 Add Expense",
        type="primary",
        use_container_width=True
    )


# =========================================================
# ADD EXPENSE PROCESSING
# =========================================================

if submit:

    error = validate_expense(
        expense_name,
        amount,
        category,
        expense_date
    )


    if error:

        st.error(error)


    elif add_expense(
        expense_name,
        amount,
        category,
        expense_date,
        description
    ):

        st.success(
            "Expense added successfully!"
        )

        st.rerun()


    else:

        st.error(
            "Could not save the expense."
        )


# =========================================================
# EDIT EXPENSE
# =========================================================

if st.session_state.edit_id is not None:

    expense_to_edit = next(
        (
            expense
            for expense in expenses
            if expense.get("id")
            == st.session_state.edit_id
        ),
        None
    )


    if expense_to_edit:

        st.markdown(
            '<div class="section-title">'
            '✏️ Edit Expense'
            '</div>',
            unsafe_allow_html=True
        )


        with st.form("edit_form"):

            col1, col2 = st.columns(2)


            with col1:

                edit_name = st.text_input(
                    "Expense Name *",
                    value=expense_to_edit.get(
                        "name",
                        ""
                    )
                )


                edit_amount = st.text_input(
                    "Amount *",
                    value=str(
                        expense_to_edit.get(
                            "amount",
                            ""
                        )
                    )
                )


                current_category = (
                    expense_to_edit.get(
                        "category",
                        "Other"
                    )
                )


                edit_categories = (
                    CATEGORIES
                    if current_category
                    in CATEGORIES
                    else
                    CATEGORIES
                    + [current_category]
                )


                edit_category = st.selectbox(
                    "Category *",
                    edit_categories,
                    index=edit_categories.index(
                        current_category
                    )
                )


            with col2:

                try:

                    current_date = (
                        date.fromisoformat(
                            str(
                                expense_to_edit.get(
                                    "date",
                                    date.today()
                                )
                            )
                        )
                    )

                except ValueError:

                    current_date = date.today()


                edit_date = st.date_input(
                    "Date *",
                    value=current_date
                )


                edit_description = st.text_area(
                    "Description",
                    value=expense_to_edit.get(
                        "description",
                        ""
                    ),
                    height=122
                )


            col_a, col_b = st.columns(2)


            with col_a:

                update_button = (
                    st.form_submit_button(
                        "✓ Update Expense",
                        type="primary",
                        use_container_width=True
                    )
                )


            with col_b:

                cancel_button = (
                    st.form_submit_button(
                        "Cancel",
                        use_container_width=True
                    )
                )


        if update_button:

            error = validate_expense(
                edit_name,
                edit_amount,
                edit_category,
                edit_date
            )


            if error:

                st.error(error)


            elif update_expense(
                st.session_state.edit_id,
                edit_name,
                edit_amount,
                edit_category,
                edit_date,
                edit_description
            ):

                st.session_state.edit_id = None

                st.success(
                    "Expense updated successfully!"
                )

                st.rerun()


            else:

                st.error(
                    "Could not update the expense."
                )


        if cancel_button:

            st.session_state.edit_id = None

            st.rerun()


# =========================================================
# EXPENSE HISTORY
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📋 Expense History'
    '</div>',
    unsafe_allow_html=True
)


if expenses:

    display_df = pd.DataFrame(
        expenses
    )


    required_columns = [
        "id",
        "name",
        "amount",
        "category",
        "date",
        "description"
    ]


    for column in required_columns:

        if column not in display_df.columns:

            display_df[column] = ""


    display_df = display_df[
        required_columns
    ].copy()


    display_df.columns = [
        "ID",
        "Expense",
        "Amount (₹)",
        "Category",
        "Date",
        "Description"
    ]


    display_df["Amount (₹)"] = (
        display_df["Amount (₹)"]
        .map(
            lambda value:
            f"₹{float(value):,.2f}"
        )
    )


    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )


    # Edit/Delete controls

    for expense in expenses:

        col1, col2, col3 = st.columns(
            [5, 1, 1]
        )


        with col1:

            st.write(
                f"**{expense.get('name', 'Unnamed')}** "
                f"· {expense.get('category', 'Other')} "
                f"· ₹{float(expense.get('amount', 0)):,.2f} "
                f"· {expense.get('date', '')}"
            )


        with col2:

            if st.button(
                "✏️ Edit",
                key=f"edit_{expense['id']}",
                use_container_width=True
            ):

                st.session_state.edit_id = (
                    expense["id"]
                )

                st.rerun()


        with col3:

            if st.button(
                "🗑️ Delete",
                key=f"delete_{expense['id']}",
                use_container_width=True
            ):

                if delete_expense(
                    expense["id"]
                ):

                    st.success(
                        "Expense deleted."
                    )

                    st.rerun()


else:

    st.info(
        "No expenses yet. Add your first expense above "
        "to get started."
    )


# =========================================================
# SPENDING INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">'
    '📊 Spending Insights'
    '</div>',
    unsafe_allow_html=True
)


chart1, chart2 = st.columns(2)


# =========================================================
# CATEGORY CHART
# =========================================================

with chart1:

    st.markdown(
        '<div class="chart-panel">'
        '<div class="chart-title">'
        '🏷️ Expenses by Category'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    if expenses:

        category_totals = defaultdict(float)


        for expense in expenses:

            category_totals[
                expense.get(
                    "category",
                    "Other"
                )
            ] += float(
                expense.get(
                    "amount",
                    0
                )
            )


        category_data = pd.DataFrame(
            list(
                category_totals.items()
            ),
            columns=[
                "Category",
                "Amount"
            ]
        )


        st.bar_chart(
            category_data.set_index(
                "Category"
            ),
            use_container_width=True
        )


    else:

        st.caption(
            "Add expenses to see the category chart."
        )


# =========================================================
# DATE CHART
# =========================================================

with chart2:

    st.markdown(
        '<div class="chart-panel">'
        '<div class="chart-title">'
        '📅 Expenses by Date'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    if expenses:

        date_totals = defaultdict(float)


        for expense in expenses:

            expense_date = str(
                expense.get(
                    "date",
                    date.today()
                )
            )


            date_totals[
                expense_date
            ] += float(
                expense.get(
                    "amount",
                    0
                )
            )


        date_data = pd.DataFrame(
            list(
                date_totals.items()
            ),
            columns=[
                "Date",
                "Amount"
            ]
        )


        date_data["Date"] = pd.to_datetime(
            date_data["Date"],
            errors="coerce"
        )


        date_data = (
            date_data
            .dropna(subset=["Date"])
            .sort_values("Date")
        )


        if not date_data.empty:

            st.line_chart(
                date_data.set_index(
                    "Date"
                ),
                use_container_width=True
            )

        else:

            st.caption(
                "No valid dates available for the chart."
            )


    else:

        st.caption(
            "Add expenses to see the date chart."
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")


st.markdown(
    '<div class="footer">'
    '💸 Expense Tracker · Python + Streamlit + JSON'
    '</div>',
    unsafe_allow_html=True
)