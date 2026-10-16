from app import create_app

app = create_app() #llama a la funcion crear app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
