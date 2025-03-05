# texto plano versus data estructurada

Dan Luu, en [The growth of command line options](https://danluu.com/cli-complexity/) afirma que:

 > 
 > If structured data or objects were passed around, formatting could be left to a final formatting pass. But, with plain text, the formatting and the content are intermingled; because formatting can only be done by parsing the content out, it's common for commands to add formatting options for convenience. Alternately, formatting can be done when the user leverages their knowledge of the structure of the data and encodes that knowledge into arguments to `cut`, `awk`, `sed`, etc. (also using their knowledge of how those programs handle formatting; it's different for different programs and the user is expected to, for example, [know how `cut -f4` is different from `awk '{ print $4 }'`](https://unix.stackexchange.com/a/132322/261842)[2](https://danluu.com/cli-complexity/#fn:T)). That's a lot more hassle than passing in one or two arguments to the last command in a sequence and it pushes the complexity from the tool to the user.
 > 
 > People sometimes say that they don't want to support structured data because they'd have to support multiple formats to make a universal tool, but they already have to support multiple formats to make a universal tool. Some standard commands can't read output from other commands because they use different formats, `wc -w` doesn't handle Unicode correctly, etc. Saying that "text" is a universal format is like saying that "binary" is a universal format.
