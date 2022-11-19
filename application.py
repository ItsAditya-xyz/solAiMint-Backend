from app.main import application

# UNCOMMENT THIS IMPORT TO ENABLE API ROUTES IN api.py


if __name__ == "__main__":
    # make the app go live on all
    application.debug = False
    application.run()
