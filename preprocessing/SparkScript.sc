def getDay(d: Int): String = if (d < 10) s"0$d" else d.toString
def getMonth(m: Int): String = m match {
  case 1 => "january"
  case 2 => "february"
  case 3 => "march"
  case 4 => "april"
  case 5 => "may"
  case 6 => "june"
  case 7 => "july"
  case 8 => "august"
  case 9 => "september"
  case 10 => "october"
}
def getUniqueLocations(day: Int, month: Int): Array[String] = { 
  try {
    val ap = sqlContext.jsonFile(s"hdfs:///datasets/goodcitylife/${getMonth(month)}/harvest3r_twitter_data_${getDay(day)}-${getDay(month)}_0.json")
    ap.select("_source.source_location").distinct.map(_.getString(0)).collect
  } catch {
    case _ => Array[String]()
  }
}
def outputFile(arr: Array[String], cnt: Int): Unit = {
  import java.io._
  val bw = new BufferedWriter(new OutputStreamWriter(
    new FileOutputStream(s"loc${cnt}.txt"), "UTF-8"))
  arr.foreach(x => {bw.write(x); bw.write("\n")})
  bw.close()
}
def processDays(days: IndexedSeq[Int], month: Int, id: Int): Unit = {
  val locs = days.map(x => getUniqueLocations(x, month)).flatten.distinct
  outputFile(locs.toArray, id)
}


// val days = (1 to 30).map(getDay)
// val months = (1 to 6).map(getDay)
// days.map(x => getUniqueLocations(x, "04"))
// processDays(22 to 30, 4, 43)
// processDays(15 to 31, 1, 1)

/* How to run spark-shell
spark-shell --driver-memory 16G --packages "org.json4s:json4s-native_2.10:3.2.10,org.json4s:json4s-jackson_2.10:3.2.10"
Copy paste Main.scala (except the package name) into the shell.
For preprocessing the data of march use the following command:
Main.preprocess(3)
A similar thing can be used for other months.
*/