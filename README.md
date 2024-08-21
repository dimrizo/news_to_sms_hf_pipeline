# Automated News Scraping and Content Generation Python project

## Project Overview

This Python project automates the process of scraping news articles, generating summaries and extracting keywords, creating images, and sending it all together via SMS to an end-user. It leverages various Python libraries and APIs, including web scraping tools, HuggingFace models for natural language processing and image generation, Google Cloud Storage for hosting images, and Twilio for SMS notifications.

## Features

- **Web Scraping:** Extracts news articles' content from a predefined list of URLs using custom scraping utilities.
- **Content Processing:** Generates summaries, extracts keywords, and creates hashtags for social media engagement.
- **Image Generation:** Produces relevant images based on article content using HuggingFace's text-to-image models.
- **Cloud Integration:** Uploads generated images to Google Cloud Storage (GCS) for accessible hosting.
- **Notification System:** Sends SMS notifications containing article details and image links from GCS via Twilio's messaging service.

## Requirements

- **Python:** 3.x
- **APIs and Services:**
  - [HuggingFace API](https://huggingface.co/) for NLP and image generation models.
  - [Google Cloud Storage](https://cloud.google.com/storage) for storing and serving images.
  - [Twilio API](https://www.twilio.com/) for sending SMS messages.

## Project Structure

- **`main.py`**: The application's entry point orchestrating all operations.
- **`scrape_for_news.py`**: Contains functions and classes for web scraping tasks.
- **`upload_img_to_gcs.py`**: Manages the uploading of generated images to Google Cloud Storage.
- **`msg_sender_twilio_sms.py`**: Handles sending SMS messages via Twilio API.
- **`hf_model_wrappers.py`**: Wraps HuggingFace models for summarization, keyword extraction, and text-to-image generation.
- **`io_files/`**: Directory for input and output files used during processing.
- **`requirements.txt`**: Lists all Python dependencies required for the project.

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**
    ```bash
    git checkout -b feature/YourFeature
    ```
3. **Commit Your Changes**
    ```bash
    git commit -m "Add your message here"
    ```
4. **Push to the Branch**
    ```bash
    git push origin feature/YourFeature
    ```
5. **Open a Pull Request**

For major changes, please open an issue first to talk about what you'd like to change.

## License

This project is licensed under the [Apache-v2.0 License](LICENSE).

## Contact

**Dimitris Rizopoulos**  
Email: [dimrizopoulos@gmail.com](mailto:dimrizopoulos@gmail.com)

Feel free to reach out with any questions or for collaboration opportunities.
