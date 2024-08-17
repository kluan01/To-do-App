from website import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True) # Allows website to run only when clicked to run