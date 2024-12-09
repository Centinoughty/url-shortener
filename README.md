# URL Shortener

A URL shortener built with **Express.js** and **MongoDB**. This project includes the following features:

- Ad display after 10 hits
- Daily hit limit of 20 per URL
- Collision-free operation

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Centinoughty/url-shortener.git
   ```

2. Navigate to the project directory:

```bash
cd url-shortener
```

3. Install dependencies

```bash
npm install
```

4. Set up MongoDB (local or cloud service like MongoDB Atlas).

5. Run the application:

```bash
npm start
```

## Features

- **URL shortening**: Create custom short URLs.
- **Hit tracking**: Monitor and limit daily hits.
- **Ad functionality**: Show ads after a set number of hits.
- **Collision-free**: Ensures no duplicate short URLs.

## License

This project is licensed under the [MIT License](LICENSE).
