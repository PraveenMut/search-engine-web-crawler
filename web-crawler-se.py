## Begin with opening the URL
def get_page(url):
    if url in cache:
        return cache[url]
    else:
        return None

## Retrieve links from the specified URL
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1: 
        return None, 0
    start_quote = page.find('"', start_link)
    end_quote = page.find('"', start_quote + 1)
    url = page[start_quote + 1:end_quote]
    return url, end_quote

## Recursive method to get all links from the get_next_target and store them in an array
## This represents an array with all the retrieved links from the specified URL
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)
        if url:
            links.append(url)
            page = page[endpos:]
        else:
            break
    return links

## Special Helper method to discard duplicate links in the array created by 
## the get_all_links method
def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)


## Add the associated words to the crawled index, thereby creating an index of keywords in a dictionary with the associated URLs.
## This in essence creates a search index that it can searched through by another method
## This replaces 
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

def add_to_index(index, keyword, url):
    if keyword in index:
        index[keyword].append(url)
    else:
        index[keyword] = [url]


## Special lookup method that retrieves the result from the index array
## created by add_to_index method
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

## THE MAIN METHOD
## Uses the first methods of retrieving the page to crawl, finding the URL in the page
## pushing such urls into an array, adding the page into an index, and then retrieving the outlinks through
## the get_all_links method. 

## This then pushed into a dictionary that uses the outlinks generated from get_all_links
## as the values and the page being the key that it is on as the key.

## This consolidates all of the concepts learned from the previous exercises by 
## creating an index from the links into a index assocated by a keyword and then
## using the link to build a "graph" or a dictionary that contains the outlinks.

## Summary: Link Retriever Get Page --> Get Links --> Store links in an array
## Search Engine Builiding: Refer to previous steps --> Add links to Index --> Create a graph with outlinks -->
## Rank page using algorithm devised by Google. 

## an additional method then consequently rank the webpages

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]
    crawled = []
    graph = {}  ## a dictionary that lists a key of the url and what pages it links to as an outlink
    index = {} 
    while tocrawl: 
        page = tocrawl.pop()
        if page not in crawled:
            content = get_page(page)
            add_page_to_index(index, page, content)
            outlinks = get_all_links(content)
            graph[page] = outlinks
            union(tocrawl, outlinks) ## union helper method used to remove duplicates
            crawled.append(page)
    return index, graph


## an earlier version of web crawl just using arrays
# def crawl_web(seed):
#     tocrawl = [seed]
#     crawled = []
#     while tocrawl:
#         page = tocrawl.pop()
#         if page not in crawled:
#             union(tocrawl, get_all_links(get_page(page)))
#             crawled.append(page)
#     return crawled


### An efficient sorting algorithm using in-place sorting with O(n * log(n)) time complexity
### in average computational time complexity. Space complexity O(n). Worst case O(n^2) as 
### the pivot is always selected at the end of the array. Future adjustments: select pivot randomly.

# tester array
arr = [7,6,5,4,3,2,1,0]

# partition (pivot) procedure
def partition(arr, start, end): 
  pivot = arr[end]
  partitionIndex = start
  i = start
  while i < end:
    if arr[i] <= pivot:
      arr[i],arr[partitionIndex] = arr[partitionIndex],arr[i]
      partitionIndex += 1
      i += 1
    else:
      i += 1
  arr[end],arr[partitionIndex]  = arr[partitionIndex],arr[end]
  return partitionIndex

# parent Quicksort algorithm
def quickSort(arr, start, end):
  if (start < end):
    partitionIndex = partition(arr, start, end)
    quickSort(arr, start, partitionIndex-1)
    quickSort(arr, partitionIndex+1, end)

## testers
n = len(arr)
quickSort(arr, 0, n-1)
for i in range(n): # print the elements in a new line
  print arr[i]

## Extra Method to rank the pages according to how many interconnected pages originally devised by Google (I did not come up with this lol).
## are present on that page. I.e., if a page has many outlinks but little inlinks, it will be ranked poorly
## Similarly, if a page has little outranks it will also rank less than optimal.
## However, many inlinks are better than many outlinks with no connections in.

def compute_ranks(graph):
    d = 0.8 # damping factor
    num_of_iterations = 10
    ranks = {}
    num_of_pages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / num_of_pages
    
    for i in range(0, num_of_iterations):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + (ranks[node] * d)/len(graph[page])
            newranks[page] = newrank
        ranks = newranks
    return ranks
    