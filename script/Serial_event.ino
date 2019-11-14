void serialEvent() {
  if (Serial.available() != 0) {
    String input_data = Serial.readStringUntil('\n');
    //    Serial.println(input_data);
    String initial_word = getValue(input_data, ' ', 0);

    // Отправить
    if (initial_word == "M") {
      done_flag = false;
      int number_of_motors = getValue(input_data, ' ', 1).toInt();
      for (int i = 2; i <= number_of_motors + 1; i++) {
        String motor = getValue(input_data, ' ', i);
        String motor_name = getValue(motor, ':', 0);
        int pos = getValue(motor, ':', 1).toInt();
        if (debug)Serial.println("Moveto " + motor_name + " " + String(pos));
        if (motor_name == "M1")m1.moveTo(pos);
        if (motor_name == "M2")m2.moveTo(pos);
        if (motor_name == "M3")m3.moveTo(pos);
        if (motor_name == "M4")m4.moveTo(pos);
        if (motor_name == "M5")m5.moveTo(pos);
        if (motor_name == "M6")m6.moveTo(pos);
        if (motor_name == "M7")m7.moveTo(pos);
        if (motor_name == "M8")m8.moveTo(pos);
        if (motor_name == "M9")m9.moveTo(pos);
        if (motor_name == "M10")m10.moveTo(pos);
      }
    }

    // Скорость
    else if (initial_word == "S") {
      done_flag = false;
      int number_of_motors = getValue(input_data, ' ', 1).toInt();
      for (int i = 2; i <= number_of_motors + 1; i++) {
        String motor = getValue(input_data, ' ', i);
        String motor_name = getValue(motor, ':', 0);
        int speed = getValue(motor, ':', 1).toInt();
        if (debug)Serial.println("Speed " + motor_name + " " + String(speed));
        if (motor_name == "M1")m1.setMaxSpeed(speed);
        if (motor_name == "M2")m2.setMaxSpeed(speed);
        if (motor_name == "M3")m3.setMaxSpeed(speed);
        if (motor_name == "M4")m4.setMaxSpeed(speed);
        if (motor_name == "M5")m5.setMaxSpeed(speed);
        if (motor_name == "M6")m6.setMaxSpeed(speed);
        if (motor_name == "M7")m7.setMaxSpeed(speed);
        if (motor_name == "M8")m8.setMaxSpeed(speed);
        if (motor_name == "M9")m9.setMaxSpeed(speed);
        if (motor_name == "M10")m10.setMaxSpeed(speed);
      }
    }

    // Акселерация
    else if (initial_word == "A") {
      done_flag = false;
      int number_of_motors = getValue(input_data, ' ', 1).toInt();
      for (int i = 2; i <= number_of_motors + 1; i++) {
        String motor = getValue(input_data, ' ', i);
        String motor_name = getValue(motor, ':', 0);
        int acceleration = getValue(motor, ':', 1).toInt();
        if (debug)Serial.println("Acceleration " + motor_name + " " + String(acceleration));
        if (motor_name == "M1")m1.setAcceleration(acceleration);
        if (motor_name == "M2")m2.setAcceleration(acceleration);
        if (motor_name == "M3")m3.setAcceleration(acceleration);
        if (motor_name == "M4")m4.setAcceleration(acceleration);
        if (motor_name == "M5")m5.setAcceleration(acceleration);
        if (motor_name == "M6")m6.setAcceleration(acceleration);
        if (motor_name == "M7")m7.setAcceleration(acceleration);
        if (motor_name == "M8")m8.setAcceleration(acceleration);
        if (motor_name == "M9")m9.setAcceleration(acceleration);
        if (motor_name == "M10")m10.setAcceleration(acceleration);
      }
    }

    // ХОУМинг
    else if (initial_word == "H") {
      done_flag = false;
      int number_of_motors = getValue(input_data, ' ', 1).toInt();
      for (int i = 2; i <= number_of_motors + 1; i++) {
        String motor_name = getValue(input_data, ' ', i);
        if (debug)Serial.println("Home " + motor_name);
        if (motor_name == "M1") {
          motorAutohome(m1, m1e);
          m1.setCurrentPosition(0);
        }
        if (motor_name == "M2") {
          motorAutohome(m2, m2e);
          m2.setCurrentPosition(0);
        }
        if (motor_name == "M3") {
          motorAutohome(m3, m3e);
          m3.setCurrentPosition(0);
        }
        if (motor_name == "M4") {
          motorAutohome(m4, m4e);
          m4.setCurrentPosition(0);
        }
        if (motor_name == "M5") {
          motorAutohome(m5, m5e);
          m5.setCurrentPosition(0);
        }
        if (motor_name == "M6") {
          motorAutohome(m6, m6e);
          m6.setCurrentPosition(0);
        }
        if (motor_name == "M7") {
          motorAutohome(m7, m7e);
          m7.setCurrentPosition(0);
        }
        if (motor_name == "M8") {
          motorAutohome(m8, m8e);
          m8.setCurrentPosition(0);
        }
        if (motor_name == "M9") {
          motorAutohome(m9, m9e);
          m9.setCurrentPosition(0);
        }
        if (motor_name == "M10") {
          motorAutohome(m10, m10e);
          m10.setCurrentPosition(0);
        }
      }
    }

    // Инвертирование осей
    else if (initial_word == "invert") {
      done_flag = false;
      int number_of_motors = getValue(input_data, ' ', 1).toInt();
      for (int i = 2; i <= number_of_motors + 1; i++) {
        String motor_name = getValue(input_data, ' ', i);
        if (debug)Serial.println("invert " + motor_name);
        if (motor_name == "M1")m1.setPinsInverted(m1d);
        if (motor_name == "M2")m2.setPinsInverted(m2d);
        if (motor_name == "M3")m3.setPinsInverted(m3d);
        if (motor_name == "M4")m4.setPinsInverted(m4d);
        if (motor_name == "M5")m5.setPinsInverted(m5d);
        if (motor_name == "M6")m6.setPinsInverted(m6d);
        if (motor_name == "M7")m7.setPinsInverted(m7d);
        if (motor_name == "M8")m8.setPinsInverted(m8d);
        if (motor_name == "M9")m9.setPinsInverted(m9d);
        if (motor_name == "M10")m10.setPinsInverted(m10d);
      }
    }

    // Утилиты

    else if (initial_word == "HTEST") {
      done_flag = false;
      int times = getValue(input_data, ' ', 1).toInt();
      
      motorAutohome(m1, m1e);
      m1.setCurrentPosition(0);
      m1.moveTo(100);
      while (m1.distanceToGo() != 0) m1.run();
      m1.setCurrentPosition(0);

      
      for (int i = 0; i < times; i++) {
        m1.moveTo(0);
        while (m1.distanceToGo() != 0) m1.run();
        
        m1.setSpeed(-500);
        while (true) {
          if (digitalRead(m1e) == 1) {
            Serial.println(m1.currentPosition());
            break;
          }
          m1.runSpeed();
        }
      }
      done_flag = true;
      Serial.println("vse");
    }

    //KEK
    
    //    else if (initial_word == "HTEST") {
    //      done_flag = false;
    //      for (int i = 0; i < 10; i++) {
    //        delay(100);
    //        Serial.println(random(10, 20));
    //      }
    //      done_flag = true;
    //      Serial.println("vse");
    //    }

    else if (initial_word == "service_test") {
      serviceTest();
    }

    else if (initial_word == "debug") debug = !debug;
    else if (initial_word == "ok") Serial.println("ok");
    else {
      Serial.println("WRONG");
    }
  }
}


void motorAutohome(AccelStepper m, int endpin) {
  m.setCurrentPosition(0);

  if (digitalRead(endpin) == 1) m.moveTo(100);
  while (m.distanceToGo() != 0) m.run();

  int i = 0;
  m.setSpeed(-500);

  while (true) {
    if (digitalRead(endpin) == 1) break;
    m.runSpeed();
  }
  m.setCurrentPosition(0);
}
