# Picks
PICKS_URL="https://www.pickswise.com/nhl/best-bets/"

# Database
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_USERNAME=root
DATABASE_NAME=
DATABASE_PASSWORD=

*/1 * * * * python3 /home/ubuntu/nhlbot/main.py >> /home/ubuntu/nhlbot/output.log 2>&1

To see process log:
grep CRON /var/log/syslog
