Casa Palacoulo

TODO: -Change port (for now there is no need)
      -Maybe login interface:
        -> remember to be done
      -create a better dashboard
        -save value of door and reset from time to time
        -create a admin page
        -maybe have a excel or dashboard with openings and closings
        -see access to site (not only with login)
        -maybe incorporate gmail username ??

u = models.User(username='admin', email='admin@admin.com', password= bcrypt.generate_password_hash('admin'))

References:
    https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world
    https://nathanpjones.com/2016/02/remote-debug-gpio-on-raspberry-pi/