from website import create_app

app = create_app()

if __name__ == '__main__':
    #Esta en debug por ahora, lo sacare cuando este todo terminado :p
    app.run(debug=True)