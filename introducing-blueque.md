---
layout: presentation
title: Introducing Blueque
---

<section>
<div markdown="1">

# Introducing Blueque #

Thomas Stephens (uStudio)

</div>
</section>

<section>
<div markdown="1">

## Where we were ##

* Using Celery

* Some normal tasks

  * Hit an API, send an email, etc.

* Some very long tasks

  *  Like, hours long...

</div>
</section>

<section>
<div markdown="1">

## Problems we had ##

* Tasks restarting

  * Config problem?
  * We couldn't turn it off

* Prefetching

  * Awesome for short tasks
  * A nightmare for long tasks
  * Short tasks get "stuck" behind long ones
  * Makes it very hard to scale dynamically

* Introspection

  * What is going on and why??????

</div>
</section>

<section>
<div markdown="1">

## Things we tried ##

* Disable ACKS_LATE

  * Supposed to cause the restart-job issue when using Redis
  * It helped, but the problem didn't go away

* Make more queues

  * Separate long running tasks into their own queue
  * Still makes it hard to scale (how many "big job" nodes do you need?)
  * Where do you draw the line?

* Read the source

  1. I must be able to fix the prefetch issue
  1. What is this "kombu" thing?
  1. Crap :-(

</div>
</section>

<section>
<div markdown="1">

## Let's just write our own! ##

![I'm afraid I just blue myself](http://cdn.hotstockmarket.com/3/3a/3a56bdfd_Im-afraid-I-just-blue-myself.jpg)

How hard could it be?

</div>
</section>

<section>
<div markdown="1">

## Features we want ##

* Easily introspectable
* Resilient
* Never time out
* Simple
* Don't prefetch
* Scheduled tasks (because we use them)

</div>
</section>

<section>
<div markdown="1">

## Easily Introspectable ##

* Start with the "protocol"
* Easy to query with a few commands
* Provide lots of aggregate lists
* Keep all per-task info together
* Could implement a Blueque-compliant client in any language

</div>
</section>

<section>
<div markdown="1">

## Simplify ##

* Make it a library, not a framework

* Leave the details up to the client

  * We can build up nice things later

* Lean on Redis for atomicity guarantees

</div>
</section>

<section>
<div markdown="1">

## How does it work? ##

* The fundamental building block is `lpoprpush`
* Move task IDs between lists, representing their state
* Update ancillary data structures to make introspection easier
* Workers poll queue for things to run
* Monitors poll complete/failed lists for things to report back
* Scheduler polls for scheduled tasks

</div>
</section>

<section>
<div markdown="1">

## What was hard? ##

* Atomicity!

  * It is hard to atomically update multiple keys when you don't know which keys you want to update ahead of time.
  * Redis docs say you can't use Lua to fix this.
  * We just use transactions, and make sure the first, atomic transaction is to the single authoritative source

</div>
</section>
