import streamlit as st
import sys
import re  # Required for StreamToExpander
from market_entry_crew.crew import MarketEntryCrew

# Set the page configuration
st.set_page_config(page_title="Market Entry Assistant", page_icon="📢", layout="wide")


def icon(emoji: str):
    """Displays an emoji as a large icon."""
    st.markdown(
        f'<div style="font-size: 100px;">{emoji}</div>',
        unsafe_allow_html=True,
    )


class StreamToExpander:
    """
    Redirects stdout to a Streamlit expander.
    This class captures print statements and displays them in an expandable section with color-coded logs.
    """
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []

    def write(self, data):
        if data.strip() == "":
            return  # Ignore empty strings

        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Split the data into lines to process individually
        lines = cleaned_data.split('\n')
        for line in lines:
            styled_line = self.style_log_line(line)
            if styled_line:
                self.buffer.append(styled_line)
            else:
                self.buffer.append(line)

        # Update the expander with the styled content
        combined_text = '<br>'.join(self.buffer)
        self.expander.markdown(combined_text, unsafe_allow_html=True)
        self.buffer = []

    def flush(self):
        """Dummy flush method to comply with the file-like interface."""
        pass

    def style_log_line(self, line):
        """
        Applies styling to specific parts of the log line.
        - Agent: Blue color
        - Thought: Green color
        - Tool Output: Orange color
        - Other lines remain default
        """
        # Define styles
        styles = {
            'Agent': 'color: #1E90FF; font-size: 14px;',       # DodgerBlue
            'Thought': 'color: #32CD32; font-size: 14px;',     # LimeGreen
            'Tool Output': 'color: #FFA500; font-size: 14px;'  # Orange
        }

        # Regex patterns for matching
        patterns = {
            'Agent': r'(Agent\s*:\s*)(.*)',
            'Thought': r'(Thought\s*:\s*)(.*)',
            'Tool Output': r'(Tool Output\s*:\s*)(.*)'
        }

        for key, pattern in patterns.items():
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                label, content = match.groups()
                # Apply styling to the label
                styled_label = f'<span style="{styles[key]}">{label}</span><span style="font-size: 14px;">{content}</span>'
                return styled_label

        # If no pattern matches, return the original line
        return line


class MarketEntryApp:
    def __init__(self):
        self.output_placeholder = st.empty()

    def run_crew(self, topic, company_name):
        # Initialize the MarketEntryCrew
        crew_instance = MarketEntryCrew()
        crew = crew_instance.crew()

        # Define the inputs for the crew
        inputs = {
            'topic': topic,
            'company_name': company_name
        }

        # Kickoff the crew and capture the output
        result = crew.kickoff(inputs=inputs)
        return result


def main():
    # Display the icon and header
    icon("📢")
    st.title("📢 Market Entry Assistant")
    st.subheader("Let AI agents assist you in planning your market entry strategy!")

    # Sidebar for user inputs
    with st.sidebar:
        st.header("👇 Enter your market entry details")
        with st.form("market_entry_form"):
            topic = st.text_input(
                "What is the topic or industry you're interested in?",
                placeholder="e.g., Autonomous Drone Systems"
            )
            company_name = st.text_input(
                "Enter the company name:",
                placeholder="e.g., Airbus"
            )
            submitted = st.form_submit_button("Submit")

        st.divider()
    # If the form is submitted, run the crew
    if submitted:
        if not topic or not company_name:
            st.error("Please provide both the topic and the company name.")
        else:
            app = MarketEntryApp()
            with st.spinner("🤖 **Agents at work...**"):
                try:
                    # Create an expander to display the agent process logs
                    expander = st.expander("Agent Process Logs", expanded=True)
                    # Redirect stdout to capture print statements
                    sys.stdout = StreamToExpander(expander)

                    # Run the crew and get the result
                    result = app.run_crew(topic, company_name)

                    # Restore stdout
                    sys.stdout = sys.__stdout__

                    # Display the result
                    st.success("✅ Market Entry Plan Ready!")
                    st.subheader("Here is your Market Entry Plan")
                    st.markdown(result)
                except Exception as e:
                    st.error(f"An error occurred: {e}")
                finally:
                    # Ensure that stdout is restored even if an error occurs
                    sys.stdout = sys.__stdout__


if __name__ == "__main__":
    main()
