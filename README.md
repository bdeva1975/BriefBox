# BriefBox

BriefBox is an AI-powered email summarization tool that streamlines inbox management by extracting key information from emails using OpenAI's GPT model. It provides concise summaries, sentiment analysis, and actionable insights, making it ideal for busy professionals, customer service teams, and anyone looking to efficiently manage high email volumes.

## Features

- **AI-Powered Summarization**: Utilizes OpenAI's GPT model to generate accurate and concise email summaries.
- **Sentiment Analysis**: Detects the overall tone and sentiment of emails.
- **Key Information Extraction**: Identifies important details such as customer names, employee mentions, and action items.
- **Customizable Output**: Flexible JSON output structure that can be tailored to specific needs.

## Text to JSON Functionality

BriefBox leverages the power of Text to JSON conversion, allowing extraction of hierarchical data from unstructured content. This approach enables us to parse emails and other text documents to extract specific information based on our prompts.

### Use Cases

1. **Email Data Extraction**: 
   - Customer sentiment analysis
   - Product references
   - Employee mentions
   - Account numbers
   - Action items or requests

2. **Call Transcript Data Extraction**:
   - Key discussion points
   - Customer concerns
   - Follow-up actions

3. **Document Data Extraction**:
   - Contract terms
   - Invoice details
   - Report summaries

## Getting Started

1. Clone the repository:
   ```
   git clone https://github.com/bdeva1975/BriefBox.git
   ```

2. Install the required dependencies:
   ```
   pip install openai python-dotenv
   ```

3. Set up your OpenAI API key in a `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

4. Run the script:
   ```
   streamlit run json_app.py
   ```

## Usage

Modify the `sample_email` in the `json_lib.py` file to process your own emails, or extend the script to read emails from a file or database.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for providing the powerful GPT model
- All contributors and users of BriefBox
