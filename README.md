# milb_bios
Download and print the biographies of entire minor league baseball rosters

## Usage

First get the required libraries:
```pipenv install```

Get the teams file - this file doesn't change very often so you can keep it for months or years. Store it anywhere you want.

```
curl "https://statsapi.mlb.com/api/v1/teams/" > ./teams.json
```

Now download some team bios. We'll pass in the path to the `teams.json` file from the previous step, and also the name of the team whose player bios we'll download.

```
pipenv run python download_bios.py ./teams.json "Lehigh Valley IronPigs"
pipenv run python download_bios.py ./teams.json "Syracuse Mets"
[output snipped]
```

Finally, let's print them out. It's a lot of data, so let's grep it to see who used to play for the MLB Phillies:
```
pipenv run python read_bios.py | grep Philadelphia.Phillies
```
