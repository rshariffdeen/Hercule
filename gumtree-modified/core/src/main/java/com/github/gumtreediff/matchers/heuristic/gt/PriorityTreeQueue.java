/*
 * This file is part of GumTree.
 *
 * GumTree is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * GumTree is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with GumTree.  If not, see <http://www.gnu.org/licenses/>.
 *
 * Copyright 2020 Jean-Rémy Falleri <jr.falleri@gmail.com>
 */

package com.github.gumtreediff.matchers.heuristic.gt;

import com.github.gumtreediff.tree.Tree;

import java.util.List;
import java.util.function.Function;

/**
 * A priority queue for trees. Priority must be a metric such as the value of a child tree is always
 * less than the value of its parent. Also, if two trees are isomorphic, they must have
 * the same priority. Trees for which the metric value is less than minimumPriority are not appended
 * to the queue.
 */
public interface PriorityTreeQueue {
    Function<Tree, Integer> HEIGHT_PRIORITY_CALCULATOR = (Tree t) -> t.getMetrics().height;
    Function<Tree, Integer> SIZE_PRIORITY_CALCULATOR = (Tree t) -> t.getMetrics().size;

    static Function<Tree, Integer> getPriorityCalculator(String name) {
        if ("size".equals(name))
            return SIZE_PRIORITY_CALCULATOR;
        else if ("height".equals(name))
            return HEIGHT_PRIORITY_CALCULATOR;
        else
            return HEIGHT_PRIORITY_CALCULATOR;
    }

    /**
     * Return the list of trees with the greatest priority, and place all
     * their children in the queue.
     */
    List<Tree> popOpen();

    /**
     * Set the function that computes the priority on a given tree.
     */
    void setPriorityCalculator(Function<Tree, Integer> calculator);

    /**
     * Return the list of trees with the greatest priority.
     */
    List<Tree> pop();

    /**
     * Put the child of the tree into the priority queue.
     */
    void open(Tree tree);

    /**
     * Return the current greatest priority.
     */
    int currentPriority();

    /**
     * Set the minimum priority of a Tree to enter the queue.
     */
    void setMinimumPriority(int priority);

    /**
     * Return the minimum priority of a Tree to enter the queue.
     */
    int getMinimumPriority();

    /**
     * Return if there is any tree in the queue.
     */
    boolean isEmpty();

    /**
     * Empty the queue.
     */
    void clear();

    /**
     * Pop the provided queues until their current priorities are equals.
     * @return true if there are elements with a same priority in the queues
     *     false as soon as one queue is empty, in which case both queues are cleared.
     */
    static boolean synchronize(PriorityTreeQueue q1, PriorityTreeQueue q2) {
        while (!(q1.isEmpty() || q2.isEmpty()) && q1.currentPriority() != q2.currentPriority()) {
            if (q1.currentPriority() > q2.currentPriority())
                q1.popOpen();
            else
                q2.popOpen();
        }

        if (q1.isEmpty() || q2.isEmpty()) {
            q1.clear();
            q2.clear();
            return false;
        }
        else
            return true;
    }
}
