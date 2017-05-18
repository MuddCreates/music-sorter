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

;; Algorithm:
;; * we have some string and regex to split on
;; * we split the string by the regex
;; * we look at the first split
;; * if it doesn't start with a quote, move on
;; * if it starts with a quote, check if it ends with a quote
;; * if it ends with a quote, trim both quotes and move on
;; * if the next split ends with a quote, trim both quotes, re-join, and move on
;; * once we run out of splits, we're done

(defn split-allowing-quotes
  [s re]
  (let [re (re-pattern (str "^(" re ")"))]
    (loop [segments []
           segment ""
           quoted? false
           s s]
      (if quoted?
        (if ))
      (if-let [[_ match] (re-find s re)]))))

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
