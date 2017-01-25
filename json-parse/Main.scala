package ch.epfl.ada

import org.json4s._
import org.json4s.native.JsonMethods._
import java.io.FileReader
import java.io.BufferedReader
import java.io.FileWriter
import java.io.BufferedWriter

object Main {
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
  def filterFields(fileName: String): Unit = {
    val js = parse(new java.io.File(fileName))
    val newJs = filterFields(js)
    val doc = render(newJs)
    val str = pretty(doc)
    val pw = new java.io.PrintWriter(s"__$fileName")
    pw.println(str)
    pw.close()
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