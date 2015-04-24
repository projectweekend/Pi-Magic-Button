This program makes it easy to map physical buttons, connected to the Raspberry Pi's GPIO pins, to API end points. Details for each button are managed in a configuration file. All you really need to do is wire things up, then edit the file.

------------------------------------------------------------------------------
### Installation
------------------------------------------------------------------------------

#### Step 1: Clone this repo

```
git clone https://github.com/projectweekend/Pi-Magic-Button.git
```

#### Step 2: Run install script

From the project directory `Pi-Magic-Button/`, run the following command:

```
./install.sh
```

**NOTE:** This step will probably take several minutes to complete. When the script begins to install [Upstart](http://upstart.ubuntu.com/), you will receive a warning. It will prompt you to type the following message to confirm the installation: `Yes, do as I say!`. You must type it exactly.

#### Step 3: Reboot

```
sudo reboot
```

------------------------------------------------------------------------------
### Configuration
------------------------------------------------------------------------------

The actions for each button need to be defined in a file named: `config.yml`. The install script will create an empty one in the root of `/Pi-Magic-Button`. Here is a complete example file:

~~~yaml
success_pin: 17
failure_pin: 22
actions:
    - button_pin: 4
      api_url: https://www.something.com/api/blah
      api_method: POST
      api_data:
        some_field: 122345
        some_other_field: some string data
    - button_pin: 18
      api_url: https://www.something.com/api/test
      api_method: POST
      api_data:
        a_different_field: 77777
        another_different_field: some string data
~~~

#### Main Properties

* `success_pin`: This pin can be connected to an LED that will light up if the button's action successfully contacted the API end point.
* `failure_pin`: This pin can be connected to an LED that will light up if the button's action did not successfully contact the API end point.
* `actions`: This is an array of configurations for each button that has been wired up to the Raspberry Pi.

#### Button Properties

Each button item in the configuration file's `actions` array has 4 properties.

* `button_pin`: This is the pin connected to the button. Under the hood each button pin is initialized using a software-defined pull up resistor. When wiring up the button connect it to ground so that it will pull the pin low when pressed.
* `api_url`: This is the URL that the button will make a request to when pressed
* `api_method`: This is the HTTP request method to use with the URL: `GET`, `POST`, `PUT`, `DELETE`
* `api_data`: Each property defined in this object will be passed to the `api_url` in the body of a `POST` or `PUT` request. `GET` and `DELETE` requests will ignore this.

------------------------------------------------------------------------------
### Upstart
------------------------------------------------------------------------------

[Upstart](http://upstart.ubuntu.com/) is used to run this program in the background on the Raspberry Pi. It will automatically start on boot as well. Every time you edit the `config.yml` you will need to restart the `magic-button` service so that it can load the new configurations. Use this command:

```
sudo service magic-button restart
```

To stop the service use this command:

```
sudo service magic-button stop
```

To start it back up again, use this command:

```
sudo service magic-button start
```
