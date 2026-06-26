from app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n====================================")
    print("🔥 ARQUITETURA  ATIVA...")
    print("🌐 http://127.0.0.1:5000")
    print("====================================\n")
    app.run(debug=True, host='0.0.0.0', port=5000)