def spiral(n)
    return [0, 0] if n == 1
    n -= 2
    r = ((Math::sqrt(n + 1) - 1) / 2).floor + 1
    p = (8 * r * (r - 1)) / 2
    en = r * 2
    a = (1 + n - p) % (r * 8)
    pos = [0, 0]
    case (a / (r * 2)).floor
    when 0
      pos[0] = r
      pos[1] = (a % en) - r
    when 1
      pos[0] = r - (a % en)
      pos[1] = r
    when 2
      pos[0] = -r
      pos[1] = r - (a % en)
    when 3
      pos[0] = (a % en) - r
      pos[1] = -r
    end
    return pos
  end
  
  def distance(x, y)
    return x.abs + y.abs
  end
  
  distance(*spiral(277678))