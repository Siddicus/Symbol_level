# Coding assignment - Label refinement
<h3>Approach:</h3>
After pre-processing the image and inversing the binary values: (0-> white space, 255 -> black), the basic idea is to look for the empty arrays of y-axis bounding length over the x-axis. For example:



<p float="center">
  <img src="https://raw.githubusercontent.com/Siddicus/Symbol_level/master/mine.JPG"  />
  
  
  
  
  <img src="https://raw.githubusercontent.com/Siddicus/Symbol_level/master/box.JPG" /> 
 
</p>



Note:

- As seen in the image above, the row that bears the red and gray boxes* correspond to the relative position of the x coordinates: *x_inital*, *x_final*

## The helper functions from here:
Let's assume we obtain the list of coordinates from above sample image as:

```
arr= [1,4,5,6,8,12,16,17,33,34,40]
```
- At first, the consecutive elements are bundled together:
 
```
arr = consecutive(arr)
arr = [1, [4, 5, 6], [5, 6], 6, 8, 12, [16, 17], 17, [33, 34], 34, 40]
```
- Subsets are removed using *av_len* function:
```
arr = av_len(arr)
arr -> [1, [4, 5, 6], 8, 12, [16, 17], [33, 34], 40
```
- From all the present nested lists(if any), a single element is extracted and the default x_inital (which is 0) is appended in case it is absent:

```
arr = choose_one(arr)
arr -> [0, 1, 5, 8, 12, 17, 34, 40]
```
## Inference
Due to the two reasons inference(*symbol level mapping of coordinates*) could not be obtained in a straightforward manner:
- The presence of gray boxes indicates joined-letter and no clear-cut bifurcation. Therefore, a threshold has been set and if the relative distance between the consecutive elements of arr is greater than that, it is assumed that bifurcation between those 2 list elements could not be performed . * I can still go for the average distance and shoot arrows in the dark but it wont work mostly because: sometimes more than 2 letters are non-bifurcable*. Therefore, I have skipped the treatment of those letters from the list.
- In few images, the bounding boxes tend to trim the y_axis length, and so the characters were getting chooped up from the edge along the y_axis. 4

## A few snapshots of the results where the image and bounding boxes are apt:


<img src="https://raw.githubusercontent.com/Siddicus/Symbol_level/master/sample_result.JPG" >
