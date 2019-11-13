String getValue(String data, char separator, int index)
{
  int found = 0;
  int strIndex[] = {0, -1};
  int maxIndex = data.length() - 1;

  for (int i = 0; i <= maxIndex && found <= index; i++) {
    if (data.charAt(i) == separator || i == maxIndex) {
      found++;
      strIndex[0] = strIndex[1] + 1;
      strIndex[1] = (i == maxIndex) ? i + 1 : i;
    }
  }

  return found > index ? data.substring(strIndex[0], strIndex[1]) : "";
}

void serviceTest() {
  while (true) {
    if (Serial.available() != 0) break;
    Serial.println(
      String(digitalRead(m1e)) + " " +
      String(digitalRead(m2e)) + " " +
      String(digitalRead(m3e)) + " " +
      String(digitalRead(m4e)) + " " +
      String(digitalRead(m5e)) + " " +
      String(digitalRead(m6e)) + " " +
      String(digitalRead(m7e)) + " " +
      String(digitalRead(m8e)) + " " +
      String(digitalRead(m9e)) + " " +
      String(digitalRead(m10e)));
    delay(100);
  }
}

void checkDestination() {
  //  delay(100);
  if (done_flag == false) {
    Serial.println(
      // Координаты
      "M " +
      String(m1.currentPosition()) + " " +
      String(m2.currentPosition()) + " " +
      String(m3.currentPosition()) + " " +
      String(m4.currentPosition()) + " " +
      String(m5.currentPosition()) + " " +
      String(m6.currentPosition()) + " " +
      String(m7.currentPosition()) + " " +
      String(m8.currentPosition()) + " " +
      String(m9.currentPosition()) + " " +
      String(m10.currentPosition())

      // Концевики
      /*
       + ":" +
      String(digitalRead(m1e)) + " " +
      String(digitalRead(m2e)) + " " +
      String(digitalRead(m3e)) + " " +
      String(digitalRead(m4e)) + " " +
      String(digitalRead(m5e)) + " " +
      String(digitalRead(m6e)) + " " +
      String(digitalRead(m7e)) + " " +
      String(digitalRead(m8e)) + " " +
      String(digitalRead(m9e)) + " " +
      String(digitalRead(m10e))
      */
      );
  }
  if (done_flag == false) {
    if (
      m1.distanceToGo() == 0 and
      m2.distanceToGo() == 0 and
      m3.distanceToGo() == 0 and
      m4.distanceToGo() == 0 and
      m5.distanceToGo() == 0 and
      m6.distanceToGo() == 0 and
      m7.distanceToGo() == 0 and
      m8.distanceToGo() == 0 and
      m9.distanceToGo() == 0 and
      m10.distanceToGo() == 0
    )
    {
      done_flag = true;
      Serial.println("done");
    }
  }
}
