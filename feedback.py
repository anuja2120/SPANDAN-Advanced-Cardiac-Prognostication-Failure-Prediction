import streamlit as st
import json

def main():
    st.title('Heart Failure Prediction Feedback')

    st.write("Thank you for using our Heart Failure Prediction model!")
    st.write("If you'd like to provide feedback, please fill out the form below:")

    user_name = st.text_input("Your Name:")
    feedback = st.text_area("Feedback:", max_chars=500)

    previous_feedback = load_previous_feedback()

    if st.button("Submit Feedback"):
        if feedback:
            st.success("Thank you for your feedback, {}!".format(user_name))
            previous_feedback.append({"user": user_name, "feedback": feedback})
            save_feedback(previous_feedback)
        else:
            st.warning("Please provide your feedback before submitting.")

    if st.button("Cancel"):
        st.warning("Feedback submission cancelled.")

    display_previous_feedback(previous_feedback)

def load_previous_feedback():
    # Load previous feedback from file
    try:
        with open("feedback.json", "r") as f:
            previous_feedback = json.load(f)
    except FileNotFoundError:
        previous_feedback = []
    return previous_feedback

def save_feedback(feedback_data):
    # Save feedback to file
    with open("feedback.json", "w") as f:
        json.dump(feedback_data, f, indent=4)

def display_previous_feedback(previous_feedback):
    st.header("Previous Feedback:")
    for item in previous_feedback:
        st.write("**{}:** {}".format(item["user"], item["feedback"]))

if __name__ == "__main__":
    main()



