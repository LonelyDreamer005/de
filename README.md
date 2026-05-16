# Hadoop MapReduce – WordCount Execution Guide

## Downloads

- [TechSpot Download](https://www.techspot.com/downloads/downloadnow/189/?evp=f14a48a23bc560f5fbe81b8d83387b41&file=241)
- [Cloudera Quickstart VM](https://downloads.cloudera.com/demo_vm/virtualbox/cloudera-quickstart-vm-5.13.0-0-virtualbox.zip)
- [GitHub Repository -> ritesh](https://github.com/sairiteshdomakuntla/de)
- [GPT Link](https://chatgpt.com/c/69e4678f-4d90-83a6-b26a-bdfcf8ffd407)
- [Blog of Map Reduce](https://blog.devgenius.io/performing-word-count-with-hadoop-a-step-by-step-guide-0a44bc2adb68)

---

# Execution of `wordcount.java`

## Run Commands

```bash
wget --no-check-certificate http://raw.githubusercontent.com/arbazahmed07/wc/main/run.sh

chmod +x run.sh

bash run.sh
```

---

## Location of Code and Output

```bash
ls

cd mapreduce

ls

cat WordCount.java
```

---

## Commands to Show Sir

```bash
hdfs dfs -ls /output

hdfs dfs -cat /output/part-r-00000
```

---

# METHOD 2: Custom Java MapReduce Program

## 1. Create the Word Count Java Program

Create a new Java file:

```bash
nano WordCount.java
```

Copy and paste the following Java code:

```java
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import java.io.IOException;
import java.util.StringTokenizer;

public class WordCount {

    public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable> {
        private final static IntWritable one = new IntWritable(1);
        private Text word = new Text();

        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
            StringTokenizer itr = new StringTokenizer(value.toString());
            while (itr.hasMoreTokens()) {
                word.set(itr.nextToken());
                context.write(word, one);
            }
        }
    }

    public static class IntSumReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();

        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

    public static void main(String[] args) throws Exception {
        Configuration conf = new Configuration();
        Job job = Job.getInstance(conf, "word count");
        job.setJarByClass(WordCount.class);
        job.setMapperClass(TokenizerMapper.class);
        job.setCombinerClass(IntSumReducer.class);
        job.setReducerClass(IntSumReducer.class);
        job.setOutputKeyClass(Text.class);
        job.setOutputValueClass(IntWritable.class);
        FileInputFormat.addInputPath(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));
        System.exit(job.waitForCompletion(true) ? 0 : 1);
    }
}
```

---

## 2. Compile the Java Code

Compile the Java program using:

```bash
javac -classpath $(hadoop classpath) -d . WordCount.java
```

This will generate `.class` files inside the current directory.

---

## 3. Create a JAR File

Package the compiled files into a JAR:

```bash
jar -cvf WordCount.jar *.class
```

---

## 4. Upload Input File to HDFS

If not already uploaded:

```bash
hadoop fs -mkdir -p /user/nielit/input

hadoop fs -put data.txt /user/nielit/input/
```

Verify:

```bash
hadoop fs -ls /user/nielit/input/
```

---

## 5. Run Your Custom Word Count Program

Execute the JAR file:

```bash
hadoop jar WordCount.jar WordCount /user/nielit/input /user/nielit/output
```

---

## 6. View Output

Check the output:

```bash
hadoop fs -ls /user/nielit/output
```

To read the results:

```bash
hadoop fs -cat /user/nielit/output/part-r-00000
```

---

## 7. Download Output (Optional)

To save the output locally:

```bash
hadoop fs -get /user/nielit/output/part-r-00000 wordcount_output.txt

cat wordcount_output.txt
```
