
<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![GPL-3.0 License][license-shield]][license-url]
![Build][build-shield]
[![Version][version-shield]][version-url]


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="135" height="135">
  </a>

  <h3 align="center">Recogg</h3>

  <p align="center">
    The first-ever AI-driven, multi-platform, and scalable attendance system
    <br />
    <a href="https://github.com/ashayp22/Recogg"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/ashayp22/Recogg">View Demo</a>
    ·
    <a href="https://github.com/ashayp22/Recogg/issues">Report Bug</a>
    ·
    <a href="https://github.com/ashayp22/Recogg/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
  * [Features](#features)
  * [Architecture](#architecture)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
* [Usage](#usage)
* [Authors](#authors)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

<!-- ABOUT THE PROJECT -->
## About The Project

![Project Image](https://github.com/ashayp22/Recogg/blob/master/images/combine_images%20(2).jpg)

Even as the world continues to become more dependent on technology that can save time, money, resources, and lives, there is a lack of technological advancements in the time and attendance management field. A [recent survey](https://www.paychex.com/newsroom/news-releases/paychex-small-business-snapshot-survey-shows-most-preferred-method-of) found that 36% of small business owners have never changed their time and attendance system, which have been used to track and monitor when employees start and stop work. In fact, once a time and attendance approach is adopted, many business owners and other people don’t change their method. This means that those people are relying on the same ancient and manual systems from the 19th century. 

Although digitizing a time and attendance system may seem insignificant, digitized systems can help to ensure accuracy and minimize errors that can easily happen when employees, teachers, and students are using paper or a spreadsheet. In fact, nearly half of the respondents to the [same survey](https://www.paychex.com/newsroom/news-releases/paychex-small-business-snapshot-survey-shows-most-preferred-method-of) said that the most important reason to invest in a time keeping solution was the efficiency and accuracy of collecting time for payroll reporting. Similar to this, another [source](https://blogs.edweek.org/edweek/learning_deeply/2016/07/the_numbers_are_in_how_a_re-designed_attendance_system_in_a_small_urban_high_school_measures_up.html) stated that "A weak attendance system sabotages a school's instructional strategy and undermines teachers." Thus, while those options appear to be both simple and free, organizations that choose to use a weaker, manual system are missing out on saving time, money, and insight into their workforce that ultimately provides employees and teachers with simplified methods to record their time worked.

So, in order to prove that technology can be used to create an attendance system that can save employers and schools time, money, and resources, we created Recogg, the first-ever AI-driven, multi-platform, and scalable attendance system. Recogg uses:

* A camera and facial recognition to track attendance, which increases the efficiency and accuracy of attendance tracking
* A database and storage container to save an organization's attendance data, which provides a secure and organized structure for attendance data
* A web interface, Raspberry Pi, and LCD screen to display an organization's information, which allows users to interact and monitor the system

Recogg was developed in 7 weeks as an [internship project](https://www.itexps.net/internship-programs) and developed as a concept/prototype for future production-level projects.  Please check out the rest of the README if you want to explore our project or get Recogg running on your local machine.

### Features
The beauty of Recogg is that it uses the features of multiple components to create a fully-functioning attendance system.

#### [API](https://github.com/ashayp22/Recogg/tree/master/API)

* Accurate Facial Recognition using AWS Facial Rekognition
* Read/Write User Data to AWS DynamoDB
* Read/Write/Get Attendance Data (CSV) from AWS S3

#### [Web Interface](https://github.com/ashayp22/Recogg/tree/master/Web%20Interface)

* User Authentication
* Create/Remove Classrooms
* Add/Remove Students & Employees
* Live Attendance Tracking
* Download Attendance to Local Machine
* Responsive Design (Web and Mobile Devices)

#### [IoT](https://github.com/ashayp22/Recogg/tree/master/IoT)

* Accurate Facial Detection
* Capture Faces using Raspberry Pi Camera
* Update LCD Screen with Information
* Turn On/Off using Button
* Mobile with a Portable Battery

#### Architecture

This is the E2E architecture diagram with all of the technologies and tools:

![Architecture](https://github.com/ashayp22/Recogg/blob/master/images/Main%20Architecture.png)

### Built With
![Platform](https://img.shields.io/badge/platforms-web%20%7C%20raspberry%20pi-blue)
![Node.js](https://img.shields.io/badge/node-%3E%3D10.16.0-green)
![NPM](https://img.shields.io/badge/npm-%3E%3D6.9-orange)
![Python](https://img.shields.io/badge/python-3.6-blue)
![Bootstrap](https://img.shields.io/badge/bootstrap-%3E%3D4.0-red)
![Raspberry-Pi](https://img.shields.io/badge/raspberry--pi-4-green)
![HTML](https://img.shields.io/badge/HTML-5-yellowgreen)
![CSS](https://img.shields.io/badge/css-3-yellow)
![JavaScript](https://img.shields.io/badge/javascript-%3E%3D8-brightgreen)

This project was built using a variety of programming languages, frameworks, APIs, and databases/storage containers. Here are the technologies broken down by which component used what:

#### API

* [Python](https://www.python.org/)
* [Amazon Rekognition](https://aws.amazon.com/rekognition/?blog-cards.sort-by=item.additionalFields.createdDate&blog-cards.sort-order=desc)
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/)
* [Amazon S3](https://aws.amazon.com/s3/)

#### Web Interface

* [Node.js](https://nodejs.org/en/)
* [Bootstrap](https://getbootstrap.com)
* [HTML/CSS/JavaScript](https://html-css-js.com/)

#### IoT
* [Python](https://www.python.org/)


<!-- GETTING STARTED -->
## Getting Started

In order to get Recogg started locally, you need to assemble the 3 components individually. Please follow this order when getting started:

1. [Deploy the API](https://github.com/ashayp22/Recogg/tree/master/API)
2. [Setup Web Interface](https://github.com/ashayp22/Recogg/tree/master/Web%20Interface)
3. [Create the IoT Component](https://github.com/ashayp22/Recogg/tree/master/IoT)

After completing the previous 3 steps, you will have a local web-interface and IoT system and cloud-based API up and running. 

<!-- USAGE EXAMPLES -->
## Usage

Since Recogg was developed as a prototype, we highly encourage you to continue improving what we have created. **Make sure to list us as the original authors, especially if you use any of our code, documentation, or instructions.**

Some examples of how Recogg can be expanded:

* Swap out the Web Interface for a Raspberry Pi Interface
* Swap out the Camera, Raspberry Pi, and LCD Screen for a mobile device
* Expand the any of the components by providing additional functionalities


<!-- AUTHORS -->
## Authors

* [Ashay Parikh](https://www.linkedin.com/in/ashay-parikh-a0621619a/) - API, Web Interface (Backend)
* [Izhaan Hussain](https://www.linkedin.com/in/izhaan-hussain-0baa711a7/) - Web Interface (Frontend)
* [Sebastian DSouza](https://www.linkedin.com/in/sebastian-dsouza-975b311a2/) - IoT (Hardware)
* [Manas Gandhi](https://www.linkedin.com/in/manas-gandhi-358827199/) - IoT (Raspberry Pi)

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

Distributed under the GPL-3.0 License. See `LICENSE` for more information.

<!-- CONTACT -->
## Contact

Click [me](mailto:ashayp22@gmail.com) to send an email to the authors.


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/badge/contributors-4-yellow
[contributors-url]: https://github.com/ashayp22/Recogg/graphs/contributors
[license-shield]: https://img.shields.io/badge/license-GPL--3-blue
[license-url]: https://github.com/ashayp22/Recogg/blob/master/LICENSE.txt
[product-screenshot]: images/screenshot.png
[build-shield]: https://img.shields.io/badge/build-passing-brightgreen
[version-shield]: https://img.shields.io/badge/version-1.0-red
[version-url]: https://github.com/ashayp22/Recogg
