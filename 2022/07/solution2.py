import bisect
import enum
import sys
import textwrap
import time
import typing
import weakref


TOTAL_SPACE    = 70_000_000
REQUIRED_SPACE = 30_000_000


def main(input_lines):
    # This challenge clearly calls for a depth-first, post-order tree traversal.
    # https://en.wikipedia.org/wiki/Tree_traversal
    #
    # We could try to assume that the input commands do this for us, but that's not strictly
    # true, it could specifically avoid doing this to catch us out!
    # So we'll go about this in two phases:
    # 1. first construct the known tree
    # 2. walk the tree and get the file sizes
    # 3. find the best candidate directory
    # 
    # n.b. Java prefers the term "visit" over "walk", but we are Pythonistas.

    # First construct our root...
    root = Node(type=NodeType.DIR, size=None, name="/", parent=None, children={})
    root.parent = weakref.ref(root)
    current_node = root

    # ...and create a stack to keep track of our location (for ease of access, we could also
    # get this by traversing backwards through all ancestors).
    path_stack = [""]
    for line in input_lines:
        if line[:1] == "$":
            # Split the line up with space delimiting. We're assuming no quoting or escaping
            # for now, otherwise we'll have to start building a full tokenizer and abstract
            # syntax tree.
            # 
            # https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization
            # https://en.wikipedia.org/wiki/Abstract_syntax_tree
            _, operator, *operands = line.rstrip('\n').split(" ")
            if operator == "cd":
                if operands[0] == "/":
                    current_node = root
                    path_stack.clear()
                    path_stack.append("")
                elif operands[0] in current_node.children:
                    child = current_node.children[operands[0]]
                    assert child.type == NodeType.DIR, "Cannot change directory into a file: {}/{}".format('/'.join(path_stack), operands[0])
                    current_node = child
                    path_stack.append(operands[0])
                elif operands[0] == "..":
                    current_node = current_node.parent()
                    path_stack.pop()
            elif operator == "ls":
                # we don't do anything special with this
                pass
        else:
            # all other lines are directory listing outputs
            size_or_type, name = line.rstrip('\n').split(" ", 1)
            if size_or_type == "dir":
                node_type = NodeType.DIR
                size = None
            else:
                node_type = NodeType.FILE
                size = int(size_or_type)
            if name not in current_node.children:
                current_node.children[name] = Node(type=node_type, size=size, name=name, children={}, parent=weakref.ref(current_node))

    # Now walk the tree to calculate the sizes. Could use a `set` here, but let's use a list and keep it
    # ordered on insert.
    _, dir_sizes = size_calculation_walker_reducer(root, [])

    # Now we've got all the sizes, figure out how much free space there is already, and what our target
    # deletion size is
    free_space = TOTAL_SPACE - root.size
    target_size = REQUIRED_SPACE - free_space

    # Then find the closest match in our list of directory sizes
    target_dir_position = bisect.bisect_left(dir_sizes, target_size)
    return dir_sizes[target_dir_position]


def size_calculation_walker_reducer(current_node, dir_sizes):
    # Shortcut if this node is a file, or it is a directory that has already been visited (shouldn't happen).
    if current_node.size != None:
        return current_node.size, dir_sizes

    total = 0
    for node in current_node.children.values():
        child_total, dir_sizes = size_calculation_walker_reducer(node, dir_sizes)
        total += child_total
        # We still need to calculate sibling sizes to add to the running total, so we can't shortcut here.
    
    current_node.size = total
    if current_node.type == NodeType.DIR:
        # `bisect` module is cool.
        bisect.insort_left(dir_sizes, total)
    return total, dir_sizes


class NodeType(enum.Enum):

    FILE = "file"
    DIR  = "dir"


# One might normally use `typing.NamedTuple` or `collections.namedtuple` here, however we can't create
# weakrefs to those types.
class Node(object):

    type:     NodeType
    size:     typing.Optional[int]
    name:     str
    children: typing.Dict[str, 'Node']
    parent:   typing.Optional[weakref.ReferenceType['Node']]
    # Why use references / weakref? Well otherwise, the child will contain a direct reference to the
    # parent, and the parent will contain a direct reference to the child: a circular reference!
    # This will stop the Python garbage collector being as effective as it can be (though in this
    # case, we want to maintain the full tree in memory, it is good practice to remember this).
    # We choose to do this with the parent because we don't want the children being destroyed
    # too early, but as long as we have a reference to the root, then all the descendents will be
    # tracked properly by garbage collection.
    #
    # https://docs.python.org/3/howto/isolating-extensions.html#garbage-collection-protocol
    # https://docs.python.org/3/library/weakref.html

    def __init__(self, **kwargs):
        # Please never do this IRL. We only do this because we complately trust every single input.
        self.__dict__.update(kwargs)


    def __repr__(self):
        # To help with debugging, and aid printing the full tree neatly
        return repr({
            "type": self.type,
            "size": self.size,
            "children": self.children
        })

    def __str__(self):
        # To help with debugging, and aid printing the full tree neatly
        self_listing  = "- {name} ({type}{size})".format(
            name=self.name,
            type=self.type.value,
            size=(", size={}".format(self.size) if self.type == NodeType.FILE else "")
        )
        child_listing = textwrap.indent('\n'.join(map(str, self.children.values())), "  ")
        return (
            self_listing
            + ('\n' if self.children else "")
            + child_listing
        )



def reader(fh):
    yield from fh
        

if __name__ == '__main__':
    fname = sys.argv[1]
    with open(fname, 'r') as fh:
        inputs = reader(fh)
        initial_stacks = next(inputs)
        start = time.monotonic_ns()
        result = main(inputs)
        end = time.monotonic_ns()

    print(result)
    print(f'Result calculated in {(end - start) / 1e3:0.3f} microseconds.', file=sys.stderr)