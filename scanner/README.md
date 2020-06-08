# contentprotect scanner

This script (`run.sh`, which runs `main.py`) is meant to be run in a cron job every hour or so.
The subreddits that the script scans are determined by the `subreddits_to_check.txt` file, but this should eventually be moved to the database.

To run this script, rename `praw.sample.ini` to `praw.ini` and fill in your [Reddit application client ID and secret](https://www.reddit.com/prefs/apps/).
When creating a new application, you should choose Script as the application type.