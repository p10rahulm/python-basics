#!/usr/bin/env ruby
require 'set'

def read_graph(file)

  puts "Start read graph"

  edges = {}
  reversed_edges = {}
  vertices = []

  IO.foreach(file) {|line| split_line = line.split

  left_vertex = split_line[0].to_i
  right_vertex = split_line[1].to_i

  vertices << left_vertex

  if edges[left_vertex]
    edges[left_vertex].push(right_vertex)
  else
    edges[left_vertex] = [right_vertex]
  end

  if reversed_edges[right_vertex]
    reversed_edges[right_vertex].push(left_vertex)
  else
    reversed_edges[right_vertex] = [left_vertex]
  end

  }

  puts "End read graph"

  return vertices.uniq.sort, edges, reversed_edges
end

def dfs_loop(vertices, edges, is_reversed)

  vertices.reverse_each { |curr_vertex|
    if not @explored_nodes.include?(curr_vertex)
      @s = curr_vertex
      dfs(edges, curr_vertex, is_reversed)
    end
  }

end

def dfs(edges, next_node, is_reversed)

  to_be_explored = []
  to_be_explored.push([next_node,1])

  @explored_nodes << next_node

  while to_be_explored.size > 0

    current_node, phase = to_be_explored.pop

    if phase == 1
      @explored_nodes << current_node

      if edges.include?(current_node)

        if not is_reversed
          @leaders[current_node] = @s
        end

        edge_found = false

        edges[current_node].each { |neighbor|
          if not @explored_nodes.include?(neighbor)
            to_be_explored.push([current_node, 1])
            to_be_explored.push([neighbor, 1])
            edge_found = true
            break
          end
        }
      else
        if not is_reversed
          @leaders[current_node] = current_node
        end
      end

      if not edge_found
        to_be_explored.push([current_node, 2])
      end
    end

    if phase == 2
      if is_reversed
        @nodes_by_finishing_time << current_node
      end
    end

  end

end

def find_top_five_leaders
  puts 'start top 5 leaders'

  counted_scc = {}
  @leaders.values.each { |leader|

    if not counted_scc.include?(leader)
      counted_scc[leader] = 1
    else
      counted_scc[leader] = counted_scc[leader] + 1
    end
  }

  sorted_scc = counted_scc.values.sort { |x, y| y <=> x }.first(5)

  while sorted_scc.length < 5
    sorted_scc << 0
  end
  puts 'end top 5 leaders'
  sorted_scc
end

def compute(file)

  @leaders = {}
  @s = nil #current leader
  @explored_nodes = Set.new []
  @nodes_by_finishing_time = []

  puts "Start algorithm"
  start = Time.now

  vertices, edges, reversed_edges = read_graph(file)

  puts 'start dfs_loop on reversed graph'
  dfs_loop(vertices, reversed_edges, true)
  puts 'end dfs_loop on reversed graph'

  puts 'start dfs_loop on regular graph'
  @explored_nodes.clear
  @s = nil

  dfs_loop(@nodes_by_finishing_time, edges, false)
  puts 'end dfs_loop on regular graph'

  sorted_scc = find_top_five_leaders()

  puts "runtime: #{Time.now - start}"
  return sorted_scc

end

max_scc = compute("data/scc.txt")
puts max_scc.to_s