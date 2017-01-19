def getUniqueLocations(day: String, month: String): Array[String] = {
  val ap = sqlContext.jsonFile(s"hdfs:///datasets/goodcitylife/april/harvest3r_twitter_data_${day}-${month}_0.json")
  ap.select("_source.source_location").distinct.map(_.getString(0)).collect
}
def getDay(d: Int): String = if (d < 10) s"0$d" else d.toString
def outputFile(arr: Array[String], cnt: Int): Unit = {
  import java.io._
  val bw = new BufferedWriter(new OutputStreamWriter(
    new FileOutputStream(s"loc${cnt}.txt"), "UTF-8"))
  arr.foreach(x => {bw.write(x); bw.write("\n")})
  bw.close()
}
def processDays(days: IndexedSeq[Int], month: Int, id: Int): Unit = {
  val locs = days.map(x => getUniqueLocations(getDay(x), getDay(month))).flatten.distinct
  outputFile(locs.toArray, id)
}


// val days = (1 to 30).map(getDay)
// val months = (1 to 6).map(getDay)
// days.map(x => getUniqueLocations(x, "04"))
// processDays(22 to 30, 4, 43)