import streamlit as st
import math

def calculate(num1, num2, operation):
    """Perform basic arithmetic operations"""
    if operation == "Add":
        return num1 + num2
    elif operation == "Subtract":
        return num1 - num2
    elif operation == "Multiply":
        return num1 * num2
    elif operation == "Divide":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2
    elif operation == "Power":
        return num1 ** num2
    elif operation == "Square Root":
        if num1 < 0:
            return "Error: Cannot calculate square root of negative number"
        return math.sqrt(num1)
    else:
        return "Invalid operation"

def main():
    st.set_page_config(
        page_title="Calculator App",
        page_icon="🧮",
        layout="centered"
    )
    
    st.title("🧮 Calculator App")
    st.markdown("---")
    
    # Sidebar for operation selection
    st.sidebar.header("Operations")
    operation = st.sidebar.selectbox(
        "Choose an operation:",
        ["Add", "Subtract", "Multiply", "Divide", "Power", "Square Root"]
    )
    
    # Main content area
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Input Numbers")
        
        if operation == "Square Root":
            num1 = st.number_input("Enter a number:", value=0.0, step=0.1)
            num2 = 0  # Not used for square root
        else:
            num1 = st.number_input("Enter first number:", value=0.0, step=0.1)
            num2 = st.number_input("Enter second number:", value=0.0, step=0.1)
    
    with col2:
        st.subheader("Result")
        
        if st.button("Calculate", type="primary"):
            result = calculate(num1, num2, operation)
            
            if isinstance(result, (int, float)):
                st.success(f"Result: {result}")
                
                # Display the calculation
                if operation == "Square Root":
                    st.info(f"√{num1} = {result}")
                else:
                    operation_symbols = {
                        "Add": "+",
                        "Subtract": "-", 
                        "Multiply": "×",
                        "Divide": "÷",
                        "Power": "^"
                    }
                    symbol = operation_symbols.get(operation, operation)
                    st.info(f"{num1} {symbol} {num2} = {result}")
            else:
                st.error(result)
    
    # Additional features
    st.markdown("---")
    st.subheader("Additional Features")
    
    # Percentage calculator
    st.write("**Percentage Calculator**")
    col3, col4, col5 = st.columns(3)
    
    with col3:
        percent_num = st.number_input("Number:", value=100.0, key="percent_num")
    with col4:
        percent_value = st.number_input("Percentage:", value=10.0, key="percent_value")
    with col5:
        if st.button("Calculate Percentage"):
            percentage_result = (percent_num * percent_value) / 100
            st.write(f"{percent_value}% of {percent_num} = {percentage_result}")
    
    # History section
    st.markdown("---")
    st.subheader("Calculation History")
    
    if 'history' not in st.session_state:
        st.session_state.history = []
    
    if st.button("Calculate", key="main_calc"):
        result = calculate(num1, num2, operation)
        if isinstance(result, (int, float)):
            history_entry = f"{num1} {operation} {num2} = {result}"
            st.session_state.history.append(history_entry)
    
    # Display history
    if st.session_state.history:
        for i, entry in enumerate(reversed(st.session_state.history[-5:])):  # Show last 5 entries
            st.write(f"{i+1}. {entry}")
        
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()
    else:
        st.write("No calculations in history yet.")

if __name__ == "__main__":
    main() 