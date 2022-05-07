# nica-timing
NICA Timing - Race Result Interface

This is a project I wrote up to monitor current output of the Race Result 12 Software.  It uses the built in Webhook feature to recive data from the Race Result 12 Server as a rider commits an action in the software.  This system is built with Python backed by a Postgres Database.

Part 1:
Data is received on port 5000 from the Race result system, it is entered into the database through parsing of the data.

Part 2:
A python webserver is run on port 500 utilizing javascript to grab data from the database for review by the timing staff
