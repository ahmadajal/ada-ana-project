package ch.epfl.ada

import org.json4s._
import org.json4s.native.JsonMethods._
import java.io.File
import java.io.FileReader
import java.io.BufferedReader
import java.io.FileWriter
import java.io.BufferedWriter

object JsonParser {
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
  def time[A](a: => A, msg: String) = {
    val start = System.nanoTime
    val result = a
    val end = (System.nanoTime - start) / (1000 * 1000)
    System.out.println(s"$msg completed in ${Console.BLUE}$end${Console.RESET} milliseconds")
    result
  }
  val fields = List("lang", "sentiment", "source_location", "published", "main")
  def readPart(fileName: String, index: Int, size: Int): Array[Char] = {
    val br = new BufferedReader(new FileReader(fileName))
    val arr = new Array[Char](size)
    br.read(arr, index, size)
    arr
  }
  def writeBytes(fileName: String, arr: Array[Char]): Unit = {
    val bw = new BufferedWriter(new FileWriter(fileName))
    bw.write(arr)
    bw.close()
  }
  def filterFields(js: JValue): JValue = {
    val children = js.children
    // val retrievedFields = fields.map(f => JObject(children.map(c => (js \ "_source").filterField(x => x._1 == "lang"))))
    val retrievedFields = children.map(c => JObject((c \ "_source").filterField(x => fields.contains(x._1))))
    JArray(retrievedFields)
  }
  def filterFields(file: File): Unit = {
    val js = parse(file)
    val newJs = filterFields(js)
    val doc = render(newJs)
    val str = pretty(doc)
    val pw = new java.io.PrintWriter(s"__${file.getName}")
    pw.println(str)
    pw.close()
  }
  def filterFields(folder: String, fileName: String): Unit = {
    filterFields(new File(folder + "/" + fileName))
  }
  def getFiles(folderName: String): Array[File] = {
    val folder = new java.io.File(folderName)
    folder.listFiles().filter(_.getName.startsWith("harvest3r_twitter_data_"))
  }
  def preprocess(monthNumber: Int): Unit = {
    val month = getMonth(monthNumber)
    val folderName = s"goodcitylife/$month"
    val files = getFiles(folderName)
    for(file <- files) {
      println(s"Started preprocessing $file")
      time(filterFields(file), s"Preprocessing $file")
    }
  }
  def getSchema(js: JValue): List[String] = {
    val schema = scala.collection.mutable.Set[String]()
    for(c <- js.children) {
      schema ++= (c \ "_source").asInstanceOf[JObject].obj.map(_._1)
    }
    schema.toList
  }
  def main(args: Array[String]) {
    // val res = parse(""" { "numbers" : [1, 2, 3, 4] } """)
    // println(res)
  }
}