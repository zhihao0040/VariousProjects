# Name: Zhi Hao Tan
# Student ID: 29650070
# GOTO line 183 for Ukkonen's algorithm for building suffix trees. Above that are all SuffixTree class-related stuff
import sys
from collections import deque
NUM_OF_CHARS = 256
class Node:
    def __init__(self, edgeStart = -1, edgeEnd = -1, idx = -1): #idx == -1 is internal node
        self.edgeStart = edgeStart
        self.edgeEnd = edgeEnd
        self.index = idx
        self.array = [None for _ in range(NUM_OF_CHARS)]
        self.suffixLink = None


class SuffixTree:
    def __init__(self, word):
        self.root = None
        self.activeNode = None
        self.activeEdge = -1
        self.activeLength = 0
        self.GLOBAL_END = [-1]
        self.word = word

    def createNode(self, edgeStart = -1, edgeEnd = -1, idx = -1):
        return Node(edgeStart, edgeEnd, idx)

    def setRoot(self, node):
        self.root = node
        self.root.suffixLink = self.root

    def createInternalNodeForUkkonen(self, pos, node, phase, extension):
        '''
        Create a new node, it will have an edge starting at the current phase, ending at Global End.
        Create a new internal node, it will have an edge starting from where the old node started, ending 1 position before where the internal is created and give it its 2 children(old node and new node)
        Change old node's edgeStart.
        '''
        # pos is where the internal node is created. 
        # phase is the new node's edge start and end that causes the internal node to be created.
        edgeStartOfOldNode = node.edgeStart
        newInternalNode = self.createNode(edgeStartOfOldNode, [pos - 1])
        newOldNode = node
        newOldNode.edgeStart = pos
        newInternalNode.array[ord(self.word[pos])] = newOldNode
        newNode = self.createNode(phase, self.GLOBAL_END, extension)
        newInternalNode.array[ord(self.word[phase])] = newNode
        newInternalNode.suffixLink = self.root
        self.activeNode.array[ord(self.word[edgeStartOfOldNode])] = newInternalNode

        return newInternalNode

    def createInternalNode(self, pos, node, phase, extension): # return the internal node connected to the old node.
        # pos is where the internal node is created. 
        # phase is the new node's edge start and end that causes the itnernal node to be created.
        edgeEndOfOldNode = node.edgeEnd
        edgeStartOfOldNode = node.edgeStart
        nodeIdxOfOld = node.index
        newInternalNode = self.createNode(edgeStartOfOldNode, pos - 1)
        newOldNode = self.createNode(pos, edgeEndOfOldNode, nodeIdxOfOld)
        newInternalNode.array[ord(self.word[pos])] = newOldNode
        newNode = self.createNode(phase, phase, extension)
        newInternalNode.array[ord(self.word[phase])] = newNode
       
        self.activeNode.array[ord(self.word[edgeStartOfOldNode])] = newInternalNode
        # self.activeNode = newOldNode

        return newInternalNode

    def naiveInsert(self, i, j):
        '''
        For the O(N^3) algorithm of building suffix trees. Ukkonen's is implemented below.
        '''
        # i = i -1
        lengthToInsert = i - j + 1
        k = j
        self.activeNode = self.root # NOT IN UKKONENS
        while lengthToInsert > 0: # change k value
            if self.activeNode.array[ord(self.word[k])] is None:
                self.activeNode.array[ord(self.word[k])] = self.createNode(i, i, j)
                lengthToInsert -= 1
                break
            lengthOfEdge = self.activeNode.array[ord(self.word[k])].edgeEnd - self.activeNode.array[ord(self.word[k])].edgeStart + 1

            if lengthOfEdge > lengthToInsert - 1:  ##### MUST BE EITHER *NEW* INTERNAL NODE OR SHOWSTOPPER
                directionToLookAt = ord(self.word[k])
                positionOfCharacterToCompareWithCurrentPhaseChar = self.activeNode.array[directionToLookAt].edgeStart + lengthToInsert - 1
                characterToCompareWithCurrentPhaseChar = self.word[positionOfCharacterToCompareWithCurrentPhaseChar]
                if characterToCompareWithCurrentPhaseChar == self.word[i]:#showstopper
                    pass

                else:
                    self.activeNode.array[directionToLookAt] = self.createInternalNode(positionOfCharacterToCompareWithCurrentPhaseChar, self.activeNode.array[directionToLookAt], i, j)
                lengthToInsert -= lengthOfEdge
                k += lengthToInsert 
            elif lengthOfEdge == lengthToInsert - 1:#either hanging off an internal node or hanging off a leaf
                directionToLookAt = ord(self.word[k])
                lengthToInsert -= lengthOfEdge
                k += lengthToInsert
                if self.activeNode.array[directionToLookAt].index == - 1: # if internal node
                    newDirectionToLookAt = ord(self.word[i])
                    if self.activeNode.array[directionToLookAt].array[newDirectionToLookAt] is None:

                        self.activeNode.array[directionToLookAt].array[newDirectionToLookAt] = self.createNode(i, i, j)
                    else:
                        self.activeEdge = directionToLookAt
                        self.activeLength +1 
                        pass # show stopper

                    self.activeNode.array[directionToLookAt].edgeEnd += 1

                lengthToInsert -= 1
                k += 1
            elif lengthOfEdge < lengthToInsert - 1: # set activeNode. Jump to next node basically.
                directionToLookAt = ord(self.word[k])
                self.activeNode = self.activeNode.array[directionToLookAt]
                lengthToInsert -= lengthOfEdge
                k += lengthOfEdge



    def naiveSuffixTreeConstruction(self, i):
        '''
        The O(N^3) algorithm of building suffix trees. Ukkonen's is implemented below.
        '''
        print(i)
        if i == -1:
            self.setRoot(self.createNode())
            self.activeNode = self.root
            self.naiveSuffixTreeConstruction(i + 1)
        elif i == len(self.word):
            pass
        else:
            for j in range(i + 1):
                self.naiveInsert(i, j)
            self.naiveSuffixTreeConstruction(i + 1)
    

    def printNodeUkko(self, node): # way to print nodes
        if self.root == node:
            print("ROOT")
        else:
            print(self.word[node.edgeStart:node.edgeEnd[0] + 1])
            if node.index != -1:
                print(node.index)


    def printNode(self, node):
        if self.root == node:
            print("ROOT")
        else:
            print(self.word[node.edgeStart:node.edgeEnd + 1])
            if node.index != -1:
                print(node.index)


    def preOrderPrint(self, node):
        if node == self.root:
            print("root")
        else:
            self.printNode(node)
        for i in range(len(node.array)):
            if node.array[i] is not None:
                self.preOrderPrint(node.array[i])


    def preOrderPrintUkko(self, node):
        if node == self.root:
            print("root")
        else:
            self.printNodeUkko(node)
        for i in range(len(node.array)):
            if node.array[i] is not None:
                self.preOrderPrintUkko(node.array[i])

    def preOrderCount(self, node, count):
        for i in range(len(node.array)):
            if node.array[i] is not None:
                count = self.preOrderCount(node.array[i], count+1)
        
        return count
          

    def UkkonenImplicitSTConstruction(self):
        '''
        Implementation of the Ukkonen's algorithm. (PS: This is my 3rd take on implementing this algorithm, yay it finally works)
        '''
        last_j = -1
        j = -1
        previousExtensionInternalNodeCreated = False
        previousExtensionNodeCreated = False
        previousNode = None
        self.setRoot(self.createNode()) # initialize our suffix tree
        self.activeNode = self.root

        # phase 0 (base case)
        self.activeNode.array[ord(self.word[0])] = self.createNode(0, self.GLOBAL_END, 0)
        j += 1
        last_j = j

        # general step.
        for phase_i in range(1, len(self.word)):
            self.GLOBAL_END[0] = phase_i # take care of Rule 1 extensions, update our GLOBAL_END, to make it mutable reference, place the int in a mutable container: a list
            j = last_j + 1
            previousExtensionInternalNodeCreated = False # we only care to build suffix links if the previousExtension of the same phase, an internal node was created
            while j <= phase_i:
                if self.activeNode.suffixLink is not None and previousExtensionNodeCreated: # if we created an explicit node, be it an internal node or just a node...surf the suffix link from current activeNode 
                    self.activeNode = self.activeNode.suffixLink # go down suffix link
                previousExtensionNodeCreated = False
                # TRAVEL TO i-1
                if self.activeLength == 0: # if no remainder
                    if (self.activeNode.array[ord(self.word[phase_i])]) is None: # at an activeNode with no remainder, just check if there is a path down the activeNode continuing as/starting from str[phase_i]
                        self.activeNode.array[ord(self.word[phase_i])] = self.createNode(phase_i, self.GLOBAL_END, j) # if not, create a new node, hang it off the internal node(be it a root node or any internal node)
                        last_j = j
                        j += 1
                        if previousExtensionInternalNodeCreated: # if we had created an internal node u on previous extension and str[j + 1...i - 1] brought us to an existing internal node...create a suffix link from u to this internal node
                            previousNode.suffixLink = self.activeNode
                        previousExtensionInternalNodeCreated = False # we did not create an internal node, rather we hanged off an internal node, a new node
                        previousExtensionNodeCreated = True # we did create a node
                        continue # we created a node, continue to next extension

                    else: # showstopper: update remainder
                        self.activeEdge = self.activeNode.array[ord(self.word[phase_i])].edgeStart
                        self.activeLength += 1
                        last_j = j - 1
                        if previousExtensionInternalNodeCreated: # if we had created an internal node u on previous extension and str[j + 1...i - 1] brought us to an existing internal node...create a suffix link from u to this internal node
                            previousNode.suffixLink = self.activeNode
                        previousExtensionInternalNodeCreated = False # we did not create an internal node, rather we hanged off an internal node, a new node
                        break
                
                lengthOfEdge = self.activeNode.array[ord(self.word[self.activeEdge])].edgeEnd[0] - self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + 1 # only will reach here if activeLength > 0, we have remainder
                while self.activeLength > lengthOfEdge: # do skip counting. While our remainder is larger than lengthOfEdge
                    
                    self.activeLength -= lengthOfEdge
                    self.activeNode = self.activeNode.array[ord(self.word[self.activeEdge])]
                    self.activeEdge += lengthOfEdge
                    
                    lengthOfEdge = self.activeNode.array[ord(self.word[self.activeEdge])].edgeEnd[0] - self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + 1

                # try to insert
                # Now you should be at the correct active node unless lengthOfEdge == activeLength. Look towards remainder
                if self.activeLength == (self.activeNode.array[ord(self.word[self.activeEdge])].edgeEnd[0] - self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + 1):
                    self.activeLength -= (self.activeNode.array[ord(self.word[self.activeEdge])].edgeEnd[0] - self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + 1)
                    # self.activeEdge += (self.activeNode.array[ord(self.word[self.activeEdge])].edgeEnd[0] - self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + 1)
                    self.activeNode = self.activeNode.array[ord(self.word[self.activeEdge])]

                # Now we will be at the CORRECT active node
                if self.activeLength == 0: # not internal node
                    if (self.activeNode.array[ord(self.word[phase_i])]) is None: # at an activeNode with no remainder, just check if there is a path down the activeNode continuing as/starting from str[phase_i]
                        self.activeNode.array[ord(self.word[phase_i])] = self.createNode(phase_i, self.GLOBAL_END, j)
                        last_j = j
                        j += 1
                        if previousExtensionInternalNodeCreated: # if we had created an internal node u on previous extension and str[j + 1...i - 1] brought us to an existing internal node...create a suffix link from u to this internal node
                            previousNode.suffixLink = self.activeNode
                        previousExtensionInternalNodeCreated = False
                        previousExtensionNodeCreated = True

                    else: # showstopper: update remainder
                        self.activeEdge = self.activeNode.array[ord(self.word[phase_i])].edgeStart
                        self.activeLength += 1
                        last_j = j - 1
                        if previousExtensionInternalNodeCreated: # if we had created an internal node u on previous extension and str[j + 1...i - 1] brought us to an existing internal node...create a suffix link from u to this internal node
                            previousNode.suffixLink = self.activeNode
                        previousExtensionInternalNodeCreated = False
                        break
                else: # internal node
                    positionOfCharacterToCompareWithCurrentPhaseChar = self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart + self.activeLength # find out where in txt to look at.
                    if ord(self.word[positionOfCharacterToCompareWithCurrentPhaseChar]) != ord(self.word[phase_i]): # if we are in the middle of an edge, and the next character wasn't the same as the character we are extending by... create an internal node
                        self.activeNode.array[ord(self.word[self.activeEdge])] = self.createInternalNodeForUkkonen(positionOfCharacterToCompareWithCurrentPhaseChar, self.activeNode.array[ord(self.word[self.activeEdge])], phase_i, j)
                        currentNode = self.activeNode.array[ord(self.word[self.activeEdge])]
                        last_j = j
                        j += 1
                        if self.activeNode == self.root: # change to look at j + 1 and since we are at j + 1 from j...our remainder's length decreases by 1
                            self.activeLength -= 1
                            self.activeEdge += 1
                        else: # do nothing, we traverse suffix link at start of extension
                            pass
                        if previousExtensionInternalNodeCreated:  # if we had created an internal node u on previous extension and str[j + 1...i - 1] brought us to an existing internal node...create a suffix link from u to this internal node
                            previousNode.suffixLink = currentNode
                        previousNode = currentNode
                        previousExtensionInternalNodeCreated = True
                        previousExtensionNodeCreated = True

                    else: # showstopper: update remainder
                        self.activeEdge = self.activeNode.array[ord(self.word[self.activeEdge])].edgeStart
                        self.activeLength += 1
                        last_j = j - 1
                        previousExtensionInternalNodeCreated = False
                        break
                
    
    def DFS_and_get_nodes(self, node):
        '''
        Using DFS, start from a specified node in the SuffixTree and traverse downwards to find all the leaves/leaf nodes, take the specified node into account as well.
        Since we are using a stack, LIFO, so we will have the leaf nodes in reverse lexicographic order
        '''
        stack = deque()
        retList = []
        stack.append(node) # take even currentNode into account
        while len(stack) > 0:
            currentNode = stack.pop()
            if currentNode.index > -1:
                retList.append(currentNode)
            
            for adjacentNode in currentNode.array:
                if adjacentNode is not None:
                    stack.append(adjacentNode)

        return retList