package ch.epfl.ada

import java.io._

object VizDataPrep {
  def extractMonthDay(fileName: String): (Int, Int) = {
    val md = fileName.takeRight("XX-XX_0.json".length).take("XX-XX".length)
    println(s"$fileName -- $md")
    (md.takeRight("XX".length).toInt, md.take("XX".length).toInt)
  }
  def getFiles(): Array[File] = {
  	val folder = new File("../viz-data")
  	folder.listFiles().flatMap(f => f.listFiles().filter(_.getName.contains("harvest3r_twitter_data")))
  }
  def fileContents(files: Array[File]): Array[((Int, Int), String)] = {
  	files.map(fn => extractMonthDay(fn.getName) -> scala.io.Source.fromFile(fn).mkString)
  }
  def writeVizData(): Unit = {
  	val pw = new java.io.PrintWriter("viz_data.js")
  	pw.println("""var data_all = new Array(13);
for(var i = 0; i < 13; i++) {
	data_all[i] = new Array(32);
}""")
  	val contents = fileContents(getFiles())
  	for(((m, d), c) <- contents) {
  		pw.println(s"data_all[$m][$d]=$c;")
  	}
  	pw.close()
  }
}