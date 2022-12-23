<?php

echo "Hello!"

$name = $_POST["name"];
$message = $_POST["message"];
$guestnumber = $_POST["guestNumber"];

require "vendor/autoload.php";

use PHPMailer/PHPMailer/PHPMailer;
use PHPMailer/PHPMailer/SMTP;


$mail = new PHPMailer();


$mail->isSMTP();
$mail->SMTPAuth = true;

$mail->Host = "smtp.gmail.com";
$mail->SMTPSecure = PHPMailer::ENCRYPTION_STARTTLS;
$mail->Port = 587;

$mail->Username = "mario.rauh13@gmail.com";
$mail->Password = "gf25b.1JTomate134!";

$mail->setFrom("mario.rauh13@gmail.com", "Mario");
$mail->addAddress("mario.rauh@t-online.de", "Mario");


$mail->Subject = "Wedding";
$mail->Body = $message;

$mail->send();

header("Location: sent.html");

?>