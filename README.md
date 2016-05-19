proximus_auto_add_vol_pack.py
===
Python script that add automatic a free volume pack for the Proximus FAI.

Please before running, check if the depends below are installed :
sudo aptitude install chromedriver xvfb python-selenium python-crontab

Please see the parameter section for usage

Initial Credits and Licence
===

Copyright (C) 2016   Tuxicoman & shakasan

This program is free software: you can redistribute it and/or modify it under the terms of the GNU Affero General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public License for more detail$

You should have received a copy of the GNU Affero General Public License along with this program.  If not, see <http://www.gnu.org/licenses/>.

Link to the post on Tuxicoman website : https://tuxicoman.jesuislibre.net/2016/05/internet-vraiment-illimite-chez-belgacomproximus.html

Link to the Github of shakasan : 
https://github.com/shakasan/bgc_add_vol_pack

Improvements - Changelog
===

* Create of object classes for more flexible usage
* Use chromedriver instead of firefox, see the variable path_browser
* Random pause of some seconds between the queries to avoids to be kicked
* Check the amount of the invoice is equal to ' 0,00'
* Add a cron job at the crontab

Parameters
===

```
usage: python proximus_auto_add_vol_pack.py "toto@proximus.be" "monSuperPwd" --debug=yes --add_cron_job=yes

Add a free extra data volume pack to Proximus FAI

positional arguments:
  user                  User proximus email
  pwd                   Password proximus

optional arguments:
  -h, --help            show this help message and exit
  --add_cron_job ADD_CRON_JOB
                        Add a job at crontab, use 'yes' or 'no' (default: no)
  --debug DEBUG         Use Xvfb to view step by step in your browser, use
                        'yes' or 'no' (default: no)

usage: python proximus_auto_add_vol_pack.py "toto@proximus.be" "monSuperPwd" --debug=yes --add_cron_job=yes
```

Demo
===

This example let to see step by step with Xvfb the progress of the script and to add a cron job at crontab for executing this script every four days

![Alt Text](https://github.com/dz0org/proximus_auto_add_vol_pack/raw/master/example_usage.gif)

View step by step with Xvfb :

![Alt Text](https://github.com/dz0org/proximus_auto_add_vol_pack/raw/master/xvfb_step_by_step.gif)

