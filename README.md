# Portrait Comparison Web Application

This web application allows users to compare and select portraits from a set of given images. It calculates and tracks ELO scores for each image based on user selections and provides the ability to export user data and image data to Excel.

## Features

- Random pairs of portraits are presented to users for comparison.
- ELO scores are calculated and updated based on user selections.
- Separate ELO scores are maintained for global, male-only, and female-only comparisons.
- User demographic data, including age and gender, is collected and stored.
- Database stores user selections, ELO scores, and demographic information.
- Export user data and image data to Excel for further analysis.
- Responsive design for optimal user experience on different devices.

## Technology Stack

- Front-End:
  - HTML/CSS with Bootstrap

- Back-End:
  - Python
  - Flask (web framework)
  - SQLite (relational database)

## Getting Started

Follow these steps to set up the application on your local machine:

1. Clone the repository:

   ```
   git clone <repository-url>
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Set up the database:
   - Create an SQLite database file.
   - Update the database connection configuration in the application's configuration file.

4. Start the Flask application:

   ```
   python app.py
   ```

5. Access the application locally:

   Open your web browser and visit [http://localhost:5000](http://localhost:5000).

## Deployment

To deploy the application to a web domain, you can follow these steps:

1. Choose a hosting provider that supports Flask applications (e.g., Heroku, AWS, DigitalOcean).

2. Set up an account and create a new application or server instance.

3. Upload the application files to the server using FTP, SFTP, or a web-based file manager.

4. Install dependencies on the server using the requirements.txt file.

5. Configure any necessary environment variables or server settings.

6. Start the Flask application on the server.

7. Configure your custom domain to point to the server's IP or domain provided by the hosting provider.

## Exporting Data

This application provides the functionality to export user data and image data to Excel files for further analysis. You can export the data using the following steps:

### User Data Export

1. Access the '/user-data-table' route of the application.

2. On the user data table page, click the "Export to Excel" button.

3. The application will download an Excel file containing the user data.

### Image Data Export

1. Access the '/foto-data-table' route of the application.

2. On the image data table page, click the "Export to Excel" button.

3. The application will download an Excel file containing the image data.

You can repeat the above steps to export the data whenever necessary.

## Contributing

Contributions to this project are welcome! If you encounter any issues or have suggestions for improvements, please submit a pull request or open an issue.

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

If you have any questions or inquiries, please contact [andrejdunda@gmail.com](mailto:andrejdunda@gmail.com).

Feel free to further customize the README file according to your project's specific details.
