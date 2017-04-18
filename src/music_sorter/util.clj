(ns music-sorter.util
  "Utility functions."
  (:require [clojure.java.shell :as shell]
            [clojure.string :as str])
  (:import [java.io IOException]))

(defn swap-exts
  [fname old new]
  (str (if (str/ends-with? fname (str "." old))
         (subs fname 0 (- (count fname) (inc (count old))))
         fname)
       "." new))

(defn sh-succeeds?
  "Run a command and return logical true if it exists and succeeds.
  The args are passed to `clojure.java.shell/sh`."
  [& args]
  (try
    (zero? (:exit (apply shell/sh args)))
    (catch IOException _)))

(defn sh-assert
  "Run a command and throw an exception if it fails. The args are
  passed to `clojure.java.shell/sh`."
  [& args]
  (try
    (let [{:keys [exit] :as info} (apply shell/sh args)]
      (or (zero? exit)
          (throw (ex-info (format "Command %s returned %d"
                                  (first (filter string? args)) exit)
                          (merge info {:args args})))))
    (catch IOException e
      (throw (ex-info (format "Command %s not found"
                              (first (filter string? args)))
                      {:args args})))))
