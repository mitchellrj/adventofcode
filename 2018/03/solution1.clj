(defstruct claim :id :x :y :w :h)

(defn read-claims
  (with-open [rdr (clojure.java.io/reader "input.txt")]
    (map 
      #(let
        [parts (rest (clojure.string/split % #"[^\d]"))]
        (apply struct (cons claim parts)))
      (line-seq rdr))))

(def get-bounds
  #(reduce
    (fn [b c] {
      :x1
        (min (get b :x1) (get c :x))
      :x2
        (max (get b :x2) (+ (get c :x) (get c :w)))
      :y1
        (min (get b :y1) (get c :y))
      :y2
        (max (get b :y2) (+ (get c :y) (get c :h)))
    })
    '({:x1 Integer/MAX_VALUE :x2 0 :y1 Integer/MAX_VALUE :y2 0})))

(defn cart [colls]
  (if (empty? colls)
    '(())
    (for [x (first colls)
          more (cart (rest colls))]
      (cons x more))))

(defn area-range [c]
  (cart (range (get c :y) (+ (get c :y) (get c :h))) (range (get c :x) (+ (get c :x) (get c :w)))))

(defn layout [claims]
  (reduce
    (fn [l c]
      (let
        [area (area-range c)]
        (reduce
          (fn [l [x, y]]
            (assoc l '(x y)
              (if
                (contains? l '(x y))
                (inc (get l '(x y))
                1
              )
          area)))
    {}
    claims))))

(count
  (filter (partial > 1) layout(read-claims)))