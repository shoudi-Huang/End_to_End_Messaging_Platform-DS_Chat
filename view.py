ó
AÈv^c           @   s#   d  d l  Z  d d d     YZ d S(   iÿÿÿÿNt   Viewc           B   sY   e  Z d  Z d d d  Z d   Z d d d  Z d   Z d	   Z d
   Z d   Z	 RS(   s4  
        A general purpose view generator
        Takes template files and dictionaries and formats them
        
        Has default header/tailer behaviour

        To display different headers when logged in, be sure to replace the
        header keyword argument when calling the function from model
    s
   templates/s   .htmlc         K   s   | |  _  | |  _ | |  _ d  S(   N(   t   template_patht   template_extensiont   global_renders(   t   selfR   R   t   kwargs(    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyt   __init__   s    		c         O   s   |  j  | |   S(   s6   
            Call defaults to load and render
        (   t   load_and_render(   R   t   argsR   (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyt   __call__   s    t   headert   tailerc   	      K   sR   |  j  |  } |  j  |  } |  j  |  } |  j d | d | d | |  } | S(   s#   
            Loads and renders templates

            :: filename :: Name of the template to load
            :: header :: Header template to use, swap this out for multiple headers 
            :: tailer :: Tailer template to use
            :: kwargs :: Keyword arguments to pass
        t   body_templatet   header_templatet   tailer_template(   t   load_templatet   render(	   R   t   filenameR
   R   R   R   R   R   t   rendered_template(    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR   "   s    			c         C   sR   |  j  | |  j } t | d  } d } x | D] } | | 7} q0 W| j   | S(   så   
            simple_render 
            A simple render using the format method
            
            :: template :: The template to use
            :: kwargs :: A dictionary of key value pairs to pass to the template
        t   rt    (   R   R   t   opent   close(   R   R   t   patht   filet   textt   line(    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR   8   s    
c   	      K   sW   |  j  | |  } |  j  | |  } |  j  | |  } | | | } |  j |  } | S(   sé    
            render
            A more complex render that joins global settings with local settings

            :: template :: The template to use
            :: kwargs :: The local key value pairs to pass to the template
        (   t   simple_rendert   global_render(	   R   R   R   R   R   t   rendered_bodyt   rendered_headt   rendered_tailR   (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR   I   s    	c         K   s"   t  j |  } | j |   } | S(   så   
            simple_render 
            A simple render using the format method
            
            :: template :: The template to use
            :: kwargs :: A dictionary of key value pairs to pass to the template
        (   t   stringt   Templatet   safe_substitute(   R   t   templateR   (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR   `   s    c         C   s   |  j  | |  j  S(   s   
            global_render 
            Renders using the global defaults
            
            :: template :: The template to use
        (   R   R   (   R   R#   (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR   m   s    (
   t   __name__t
   __module__t   __doc__R   R	   R   R   R   R   R   (    (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyR       s   					(    (   R    R    (    (    (    sY   /Users/tianqiu/OneDrive - The University of Sydney (Students)/TA/project/template/view.pyt   <module>   s   