# Contact Book Application

A full-featured contact management web application built with Flask and MongoDB.

## Features

- Add, update, and delete contacts
- Categorize contacts
- Export contacts to CSV file
- Import contacts from CSV file
- Responsive design
- MongoDB database storage

## Tech Stack

- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Flask (Python)
- **Database**: MongoDB Atlas
- **Deployment**: Vercel

## Deployment

This application is deployed on Vercel. You can access it [here](#) (replace with your Vercel deployment URL).

## Local Development

1. Clone the repository

   ```
   git clone <repository-url>
   cd contact_book
   ```

2. Create a virtual environment

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies

   ```
   pip install -r requirements.txt
   ```

4. Create a `.env` file with the following variables:

   ```
   SECRET_KEY=your_secret_key_here
   MONGO_USERNAME=your_mongodb_username
   MONGO_PASSWORD=your_mongodb_password
   MONGO_CLUSTER=your_cluster.mongodb.net
   MONGO_APP_NAME=your_app_name
   ```

5. Run the application

   ```
   python app.py
   ```

6. Open your browser and navigate to `http://localhost:5000`

## Environment Variables

- `SECRET_KEY`: Secret key for Flask sessions
- `MONGO_USERNAME`: MongoDB Atlas username
- `MONGO_PASSWORD`: MongoDB Atlas password
- `MONGO_CLUSTER`: MongoDB Atlas cluster address
- `MONGO_APP_NAME`: MongoDB application name

## Deployment on Vercel

1. Make sure you have `vercel.json` and `requirements.txt` in your project
2. Connect your GitHub repository to Vercel
3. Configure the environment variables in the Vercel dashboard
4. Deploy your application

## License

MIT
