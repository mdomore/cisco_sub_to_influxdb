<h3 align="center">Cisco Sub to influxdb</h3>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is just a script that get subscribers informations from Cisco ASR router via snmp, make some calculation and put the result in influxdb.

This is a good way to monitor your subscribers.

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

1. Create a config.json file, with this tempalte.
    ```sh
    {
        "snmp": {
            "community": "public",
            "version": "2"
            },
            "hosts": {
                "lns1": {
                    "ip": "lns1.foo.com",
                    "nb_sub": 0
                }
            },
            "influx": {
                "host": "influxdb.foo.com",
                "port": 8086,
                "type": {
                    "type_1": {
                        "nb_sub": 0,
                        "domain": "foo.com",
                        "vlan": 100,
                        "novlan": 0
                        },
                    "type_2": {
                        "nb_sub": 0,
                        "domain": "bar.com",
                        "vlan": 200,
                        "novlan": 0
                        },
                    "type_3": {
                        "nb_sub": 0,
                        "domain": "bar.com",
                        "vlan": 0,
                        "novlan": "300,200"
                        }
                    }
                }
        }
    ```
You can match user by vlan (if you use s-vlan on your ENNI) or you can match by realm (domain).
If two users use the same realm but on different vlan you can filter the vlan with the no vlan attribut.
For example : 

user1@bar.com || vlan 200 : will be count on type_2
If you don't want to count on type_3 too you need to add 200 to novlan.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* netsnmp
  ```sh
  pip install netsnmp
  ```

* netsnmp
  ```sh
  pip install json
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/mdomore/cisco_sub_to_influxdb.git
   ```

<!-- USAGE EXAMPLES -->
## Usage

Just lunch the main.py script.


<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/mdomore/cisco_sub_to_influxdb/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Project Link: [https://github.com/mdomore/cisco_sub_to_influxdb](https://github.com/mdomore/cisco_sub_to_influxdb)



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/mdomore/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/mdomore/repo/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/mdomore/repo.svg?style=for-the-badge
[forks-url]: https://github.com/mdomore/repo/network/members
[stars-shield]: https://img.shields.io/github/stars/mdomore/repo.svg?style=for-the-badge
[stars-url]: https://github.com/mdomore/repo/stargazers
[issues-shield]: https://img.shields.io/github/issues/mdomore/repo.svg?style=for-the-badge
[issues-url]: https://github.com/mdomore/repo/issues
[license-shield]: https://img.shields.io/github/license/mdomore/repo.svg?style=for-the-badge
[license-url]: https://github.com/mdomore/repo/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/mdomore
